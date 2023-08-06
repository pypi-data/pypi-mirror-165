import json
import os
import warnings
from itertools import zip_longest

import numpy as np
import pandas as pd
from IPython import embed
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.models import model_from_json
from tensorflow.keras import backend as K
import tensorflow.keras as ke
import tensorflow as tf

from qlknn.models.ffnn import determine_settings, _prescale, clip_to_bounds


def rmse(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_true - y_pred)))


class megaHornNet:
    def __init__(self, paths):
        self._HornNets = []
        self._feature_names = pd.Series([])
        self._target_names = pd.Series([])
        for i, path in enumerate(paths):
            self._HornNets.append(NDHornNet(path))
            self._target_names = self._target_names.append(
                self._HornNets[i]._target_names, ignore_index=True
            )
            for feature_name in self._HornNets[i]._feature_names:
                if feature_name not in self._feature_names.values:
                    self._feature_names = self._feature_names.append(
                        pd.Series([feature_name]), ignore_index=True
                    )

    def get_output(
        self,
        inp,
        batch_size=None,
        clip_low=False,
        clip_high=False,
        low_bound=None,
        high_bound=None,
        safe=True,
        output_pandas=True,
        shift_output_by=0,
        layer_names=None,
    ):
        if output_pandas:
            output = self._HornNets[0].get_output(
                inp,
                batch_size=batch_size,
                clip_low=clip_low,
                clip_high=clip_high,
                low_bound=low_bound,
                high_bound=high_bound,
                safe=safe,
                output_pandas=output_pandas,
                shift_output_by=shift_output_by,
                layer_names=layer_names,
            )
            for net in self._HornNets[1:]:
                output = pd.concat(
                    [
                        output,
                        net.get_output(
                            inp,
                            batch_size=batch_size,
                            clip_low=clip_low,
                            clip_high=clip_high,
                            low_bound=low_bound,
                            high_bound=high_bound,
                            safe=safe,
                            output_pandas=output_pandas,
                            shift_output_by=shift_output_by,
                            layer_names=layer_names,
                        ),
                    ],
                    axis=1,
                    copy=False,
                )
        else:
            output = []
            for net in self._HornNets:
                output.append(
                    net.get_output(
                        inp,
                        batch_size=batch_size,
                        clip_low=clip_low,
                        clip_high=clip_high,
                        low_bound=low_bound,
                        high_bound=high_bound,
                        safe=safe,
                        output_pandas=output_pandas,
                        shift_output_by=shift_output_by,
                        layer_names=layer_names,
                    )
                )
        return output

    def get_internal_constants(
        self,
        inp,
        batch_size=None,
        clip_low=False,
        clip_high=False,
        low_bound=None,
        high_bound=None,
        safe=True,
        output_pandas=True,
        shift_output_by=0,
        layer_names=None,
    ):
        """Get the c* constants from internal HornNets

        To make our life easier, we assume there are three HornNets,
        ordered like ETG, ITG, TEM. This means we have to use pandas.
        """
        if len(self._HornNets) != 3:
            raise Exception("Need to have exactely three internal HornNets")
        if not all(self._HornNets[0]._target_names == ["efeETG_GB"]):
            raise Exception("Pass ETG net as first net")
        if not all(self._HornNets[1]._target_names == ["efeITG_GB", "efiITG_GB", "pfeITG_GB"]):
            raise Exception("Pass ITG net as second net")
        if not all(self._HornNets[2]._target_names == ["efeTEM_GB", "efiTEM_GB", "pfeTEM_GB"]):
            raise Exception("Pass TEM net as third net")
        if not safe:
            raise Exception("Only implemented in safe mode")
        kwargs = {
            "batch_size": batch_size,
            "clip_low": clip_low,
            "clip_high": clip_high,
            "low_bound": low_bound,
            "high_bound": high_bound,
            "safe": safe,
            "output_pandas": output_pandas,
        }
        ETG = self._HornNets[0].get_output(
            inp, layer_names=["c1_output", "c2_output_efeETG_GB", "c3_output_efeETG_GB"], **kwargs
        )
        ETG = ETG.rename(columns={"c1_output": "c1_ETG"})
        ITG = self._HornNets[1].get_output(
            inp,
            layer_names=[
                "c1_output",
                "c2_output_efeITG_GB",
                "c2_output_efiITG_GB",
                "c3_output_efeITG_GB",
                "c3_output_efiITG_GB",
                "output_pfeITG_GB",
            ],
            **kwargs,
        )
        ITG = ITG.rename(columns={"c1_output": "c1_ITG", "output_pfeITG_GB": "pfeITG_GB"})
        TEM = self._HornNets[2].get_output(
            inp,
            layer_names=[
                "c1_output",
                "c2_output_efeTEM_GB",
                "c2_output_efiTEM_GB",
                "c3_output_efeTEM_GB",
                "c3_output_efiTEM_GB",
                "output_pfeTEM_GB",
            ],
            **kwargs,
        )
        TEM = TEM.rename(columns={"c1_output": "c1_TEM", "output_pfeTEM_GB": "pfeTEM_GB"})
        output = pd.concat([ETG, ITG, TEM], axis="columns")
        output.columns = [col[:2] + col[9:] if "output" in col else col for col in output.columns]
        # Re-order to Fortran order
        forder = [
            "c1_ETG",
            "c1_ITG",
            "c1_TEM",
            "c2_efeETG_GB",
            "c2_efeITG_GB",
            "c2_efeTEM_GB",
            "c2_efiITG_GB",
            "c2_efiTEM_GB",
            "c3_efeETG_GB",
            "c3_efeITG_GB",
            "c3_efeTEM_GB",
            "c3_efiITG_GB",
            "c3_efiTEM_GB",
            "pfeITG_GB",
            "pfeTEM_GB",
        ]
        output = output.loc[:, forder]
        if output_pandas:
            return output
        else:
            return output.values


class NDHornNet:
    def __init__(self, path, GB_scale_length=1.0, target_names_mask=None):
        self.model_from_json(path)
        self._GB_scale_length = GB_scale_length
        self._target_names_mask = target_names_mask

    def model_from_json(self, path="nn.json"):
        with open(path, "r") as file_:
            nn_dict = json.load(file_)

        self.settings = nn_dict["_parsed_settings"]
        self._feature_names = pd.Series(nn_dict["feature_names"])
        self._target_names = pd.Series(nn_dict["target_names"])

        self._feature_prescale_bias = pd.Series(
            dict(
                (k, nn_dict["prescale_bias"][k])
                for k in self._feature_names
                if k in nn_dict["prescale_bias"]
            )
        )
        self._feature_prescale_factor = pd.Series(
            dict(
                (k, nn_dict["prescale_factor"][k])
                for k in self._feature_names
                if k in nn_dict["prescale_factor"]
            )
        )
        self._target_prescale_bias = pd.Series(
            dict(
                (k, nn_dict["prescale_bias"][k])
                for k in self._target_names
                if k in nn_dict["prescale_bias"]
            )
        )
        self._target_prescale_factor = pd.Series(
            dict(
                (k, nn_dict["prescale_factor"][k])
                for k in self._target_names
                if k in nn_dict["prescale_factor"]
            )
        )

        self._feature_min = pd.Series(nn_dict["feature_min"])
        self._feature_max = pd.Series(nn_dict["feature_max"])
        self._target_min = pd.Series(nn_dict["target_min"])
        self._target_max = pd.Series(nn_dict["target_max"])

        self._branch2_names = nn_dict["special_feature"]
        self._branch1_names = nn_dict["feature_names"]
        for dim in self._branch2_names:
            self._branch1_names.remove(dim)

        self.model = ke.models.model_from_json(json.dumps(nn_dict["model"]))
        weight_dict = nn_dict["weights"]
        for layer in self.model.layers:
            layer.set_weights([np.array(el) for el in weight_dict[layer.name]])

        self.threshold_model = self.extract_ke_c1_model()

    def extract_ke_c1_model(self):
        c1_model = ke.Model(
            inputs=self.model.input[0], outputs=self.model.get_layer("c1_output").output
        )
        return c1_model

    def get_threshold(self, inp, batch_size=None):
        nn_input = inp.loc[:, self._branch1_names]
        nn_input = _prescale(
            nn_input,
            self._feature_prescale_factor[self._branch1_names].values,
            self._feature_prescale_bias[self._branch1_names].values,
        )
        nn_out = self.threshold_model.predict(nn_input.values, batch_size=batch_size)
        rescaled_out = (
            nn_out - np.atleast_2d(self._feature_prescale_bias[self._branch2_names].values)
        ) / np.atleast_2d(self._feature_prescale_factor[self._branch2_names].values)
        return rescaled_out

    def get_output(
        self,
        inp,
        batch_size=None,
        clip_low=False,
        clip_high=False,
        low_bound=None,
        high_bound=None,
        safe=True,
        output_pandas=True,
        shift_output_by=0,
        layer_names=None,
    ):
        """
        This should accept a pandas dataframe, and should return a pandas dataframe
        """
        nn_input, safe, clip_low, clip_high, low_bound, high_bound = determine_settings(
            self, inp, safe, clip_low, clip_high, low_bound, high_bound
        )

        nn_input = _prescale(
            nn_input,
            self._feature_prescale_factor.values,
            self._feature_prescale_bias.values,
        )
        # Apply all NN layers an re-scale the outputs
        if safe:
            branched_in = [
                nn_input.loc[:, self._branch1_names].values,
                nn_input.loc[:, self._branch2_names].values,
            ]
        else:
            branched_in = [
                nn_input[:, : len(self._branch1_names)],
                nn_input[:, len(self._branch1_names) :],
            ]

        if layer_names is None:
            nn_out = self.model.predict(branched_in, batch_size=batch_size)  # Get prediction
        else:
            output = np.ndarray((branched_in[0].shape[0], 0))
            layer_outputs = [
                self.model.get_layer(layer_name).output for layer_name in layer_names
            ]
            intermediate_layer_model = Model(inputs=self.model.input, outputs=layer_outputs)
            nn_out = intermediate_layer_model.predict(branched_in, batch_size=batch_size)
            if len(layer_names) == 1:
                nn_out = [nn_out]

        if layer_names is None:
            if isinstance(nn_out, np.ndarray):
                output = [nn_out]
            else:
                output = nn_out

            length = output[0].size
            scale_mask = [
                not any(prefix in name for prefix in ["df", "chie", "xaxis"])
                for name in self._target_names
            ]
            for i in range(self._target_names.size):
                output[i] -= self._target_prescale_bias.iloc[i]
                output[i] /= self._target_prescale_factor.iloc[i]
                output[i] -= shift_output_by
                output[i] = output[i].reshape(
                    length,
                )
                if self._GB_scale_length != 1.0 and scale_mask[i]:
                    output[i] /= self._GB_scale_length

            if isinstance(output, list):
                output = np.stack(output).T
            else:
                output = output[:, np.newaxis]
            output = clip_to_bounds(output, clip_low, clip_high, low_bound, high_bound)

            if output_pandas:
                output = pd.DataFrame(output, columns=self._target_names)
        else:
            if output_pandas:
                out_pds = []
                for layer_name, out in zip_longest(layer_names, nn_out):
                    if out.ndim > 2:
                        raise NotImplementedError("more than 2D output from keras layers")
                    elif out.ndim == 1 or out.shape[1] == 1:
                        out_pd = pd.DataFrame(data=out, columns=[layer_name])
                    else:
                        out_pd = pd.DataFrame(
                            data=out,
                            columns=pd.MultiIndex.from_product(
                                [[layer_name], range(out.shape[1])]
                            ),
                        )
                    out_pds.append(out_pd)
                output = pd.concat(out_pds, axis=1)
            else:
                output = np.hstack(nn_out)

        if self._target_names_mask is not None:
            output.columns = self._target_names_mask
        return output

    def get_layer_names(self):
        return [layer.name for layer in self.model.layers]


class KerasNDNN:
    def __init__(
        self,
        model,
        feature_names,
        target_names,
        feature_prescale_factor,
        feature_prescale_bias,
        target_prescale_factor,
        target_prescale_bias,
        feature_min=None,
        feature_max=None,
        target_min=None,
        target_max=None,
        target_names_mask=None,
        descale_output=True,
        debias_output=True,
    ):
        self.model = model
        self._feature_names = pd.Series(feature_names)
        self._target_names = pd.Series(target_names)
        if not isinstance(feature_prescale_factor, pd.Series):
            feature_prescale_factor = pd.Series(
                feature_prescale_factor, index=self._feature_names
            )
        if not isinstance(feature_prescale_bias, pd.Series):
            feature_prescale_bias = pd.Series(feature_prescale_bias, index=self._feature_names)
        if not isinstance(target_prescale_factor, pd.Series):
            target_prescale_factor = pd.Series(target_prescale_factor, index=self._target_names)
        if not isinstance(target_prescale_bias, pd.Series):
            target_prescale_bias = pd.Series(target_prescale_bias, index=self._target_names)
        self._feature_prescale_factor = feature_prescale_factor
        self._feature_prescale_bias = feature_prescale_bias
        self._target_prescale_factor = target_prescale_factor
        self._target_prescale_bias = target_prescale_bias
        self._descale_output = descale_output
        self._debias_output = debias_output

        if feature_min is None:
            feature_min = pd.Series({var: -np.inf for var in self._feature_names})
        self._feature_min = feature_min
        if feature_max is None:
            feature_max = pd.Series({var: np.inf for var in self._feature_names})
        self._feature_max = feature_max
        if target_min is None:
            target_min = pd.Series({var: -np.inf for var in self._target_names})
        self._target_min = target_min
        if target_max is None:
            target_max = pd.Series({var: np.inf for var in self._target_names})
        self._target_max = target_max
        self._target_names_mask = target_names_mask

    def get_output(
        self,
        inp,
        clip_low=False,
        clip_high=False,
        low_bound=None,
        high_bound=None,
        safe=True,
        output_pandas=True,
    ):
        """
        This should accept a pandas dataframe, and should return a pandas dataframe
        """
        nn_input, safe, clip_low, clip_high, low_bound, high_bound = determine_settings(
            self, inp, safe, clip_low, clip_high, low_bound, high_bound
        )

        nn_input = _prescale(nn_input, self._feature_prescale_factor, self._feature_prescale_bias)

        # Apply all NN layers
        nn_out = self.model.predict(nn_input)  # Get prediction
        output = nn_out

        if self._debias_output:
            output -= self._target_prescale_bias
        if self._descale_output:
            output /= self._target_prescale_factor

        output = clip_to_bounds(output, clip_low, clip_high, low_bound, high_bound)

        if output_pandas:
            output = pd.DataFrame(output, columns=self._target_names)

        if self._target_names_mask is not None:
            output.columns = self._target_names_mask
        return output

    def get_layer_names(self):
        return [layer.name for layer in self.model.layers]


class MichaelNN(KerasNDNN):
    def __init__(
        self,
        model,
        feature_names,
        target_names,
        feature_prescale_factor,
        feature_prescale_bias,
        target_prescale_factor,
        target_prescale_bias,
        feature_min=None,
        feature_max=None,
        target_min=None,
        target_max=None,
        target_names_mask=None,
        descale_output=True,
        debias_output=True,
    ):
        super().__init__(
            model,
            feature_names,
            target_names,
            feature_prescale_factor,
            feature_prescale_bias,
            target_prescale_factor,
            target_prescale_bias,
            feature_min=feature_min,
            feature_max=feature_max,
            target_min=target_min,
            target_max=target_max,
            target_names_mask=target_names_mask,
            descale_output=descale_output,
            debias_output=debias_output,
        )

    @classmethod
    def from_hdf5(
        cls,
        model_file,
        standardization_file,
        target_names,
        descale_output=False,
        debias_output=False,
    ):
        model = load_model(model_file, compile=False)
        model.load_weights(model_file)
        return cls.from_model(
            model,
            standardization_file,
            target_names,
            descale_output=descale_output,
            debias_output=debias_output,
        )

    @classmethod
    def from_model(
        cls,
        model,
        standardization_file,
        target_names,
        descale_output=False,
        debias_output=False,
    ):
        feature_names = pd.Series(["Zeff", "q", "smag", "An", "At", "logNustar"])

        stds = pd.read_csv(standardization_file)
        stds.set_index("name", inplace=True)
        # Was normalised to s=1, m=0
        s_t = 1
        m_t = 0
        s_sf = stds.loc[feature_names, "std"].values
        s_st = stds.loc[target_names, "std"].values
        m_sf = stds.loc[feature_names, "mean"].values
        m_st = stds.loc[target_names, "mean"].values
        if (
            np.isnan(s_sf).any()
            or np.isnan(s_st).any()
            or np.isnan(m_sf).any()
            or np.isnan(m_st).any()
        ):
            raise ValueError(
                "Could not read out standardizations for all features and targets from {!s}. Check if they are in the file!".format(
                    standardization_file
                )
            )
        feature_scale_factor = s_t / s_sf
        feature_scale_bias = -m_sf * s_t / s_sf + m_t
        target_scale_factor = s_t / s_st
        target_scale_bias = -m_st * s_t / s_st + m_t
        return cls(
            model,
            feature_names,
            target_names,
            feature_scale_factor,
            feature_scale_bias,
            target_scale_factor,
            target_scale_bias,
            descale_output=descale_output,
            debias_output=debias_output,
        )


class TwoBranchNDNN(KerasNDNN):
    def __init__(
        self,
        model,
        branch1_names,
        branch2_names,
        feature_names,
        target_names,
        feature_prescale_factor,
        feature_prescale_bias,
        target_prescale_factor,
        target_prescale_bias,
        feature_min=None,
        feature_max=None,
        target_min=None,
        target_max=None,
        target_names_mask=None,
        GB_scale_length=1.0,
        descale_output=True,
        debias_output=True,
        descale_output_together=False,
    ):
        self._GB_scale_length = GB_scale_length
        self._descale_output = descale_output
        self._debias_output = debias_output
        self._descale_output_together = descale_output_together
        self._branch1_names = branch1_names
        self._branch2_names = branch2_names

        super().__init__(
            model,
            feature_names,
            target_names,
            feature_prescale_factor,
            feature_prescale_bias,
            target_prescale_factor,
            target_prescale_bias,
            feature_min=feature_min,
            feature_max=feature_max,
            target_min=target_min,
            target_max=target_max,
            target_names_mask=target_names_mask,
            descale_output=descale_output,
            debias_output=debias_output,
        )

    @property
    def feature_names(self):
        return pd.Series(self._branch1_names + self._branch2_names)

    def get_output(
        self,
        inp,
        clip_low=False,
        clip_high=False,
        low_bound=None,
        high_bound=None,
        safe=True,
        output_pandas=True,
        shift_output_by=0,
        layer_names=None,
    ):
        """
        This should accept a pandas dataframe, and should return a pandas dataframe
        """
        nn_input, safe, clip_low, clip_high, low_bound, high_bound = determine_settings(
            self, inp, safe, clip_low, clip_high, low_bound, high_bound
        )

        nn_input = _prescale(
            nn_input,
            self._feature_prescale_factor.values,
            self._feature_prescale_bias.values,
        )
        # Apply all NN layers an re-scale the outputs
        if safe:
            branched_in = [
                nn_input.loc[:, self._branch1_names].values,
                nn_input.loc[:, self._branch2_names].values,
            ]
        else:
            branched_in = [
                nn_input[:, : len(self._branch1_names)],
                nn_input[:, len(self._branch1_names) :],
            ]

        if layer_names is None:
            nn_out = self.model.predict(branched_in)  # Get prediction
        else:
            output = np.ndarray((branched_in[0].shape[0], 0))
            layer_outputs = [
                self.model.get_layer(layer_name).output for layer_name in layer_names
            ]
            intermediate_layer_model = Model(inputs=self.model.input, outputs=layer_outputs)
            nn_out = intermediate_layer_model.predict(branched_in)
            if len(layer_names) == 1:
                nn_out = [nn_out]

        if layer_names is None:
            if isinstance(nn_out, np.ndarray):
                output = [nn_out]
            else:
                output = nn_out

            length = output[0].size
            scale_mask = [
                not any(prefix in name for prefix in ["df", "chie", "xaxis"])
                for name in self._target_names
            ]
            for i in range(self._target_names.size):
                if self._debias_output:
                    output[i] -= self._target_prescale_bias.iloc[i]
                if self._descale_output:
                    if self._descale_output_together:
                        output[i] *= self._target_prescale_factor.apply(lambda x: 1 / x).mean()
                    else:
                        output[i] /= self._target_prescale_factor.iloc[i]
                output[i] -= shift_output_by
                output[i] = output[i].reshape(
                    length,
                )
                if self._GB_scale_length != 1.0 and scale_mask[i]:
                    output[i] /= self._GB_scale_length

            if isinstance(output, list):
                output = np.stack(output).T
            else:
                output = output[:, np.newaxis]
            output = clip_to_bounds(output, clip_low, clip_high, low_bound, high_bound)

            if output_pandas:
                output = pd.DataFrame(output, columns=self._target_names)
        else:
            if output_pandas:
                out_pds = []
                for layer_name, out in zip_longest(layer_names, nn_out):
                    if out.ndim > 2:
                        raise NotImplementedError("more than 2D output from keras layers")
                    elif out.ndim == 1 or out.shape[1] == 1:
                        out_pd = pd.DataFrame(data=out, columns=[layer_name])
                    else:
                        out_pd = pd.DataFrame(
                            data=out,
                            columns=pd.MultiIndex.from_product(
                                [[layer_name], range(out.shape[1])]
                            ),
                        )
                    out_pds.append(out_pd)
                output = pd.concat(out_pds, axis=1)
            else:
                output = np.hstack(nn_out)

        if self._target_names_mask is not None:
            output.columns = self._target_names_mask
        return output


class Philipp7DNN(TwoBranchNDNN):
    def __init__(
        self,
        model,
        branch1_names,
        branch2_names,
        feature_names,
        target_names,
        feature_prescale_factor,
        feature_prescale_bias,
        target_prescale_factor,
        target_prescale_bias,
        feature_min=None,
        feature_max=None,
        target_min=None,
        target_max=None,
        target_names_mask=None,
        GB_scale_length=1.0,
        descale_output=True,
        debias_output=False,
        descale_output_together=False,
    ):
        super().__init__(
            model,
            branch1_names,
            branch2_names,
            feature_names,
            target_names,
            feature_prescale_factor,
            feature_prescale_bias,
            target_prescale_factor,
            target_prescale_bias,
            feature_min=feature_min,
            feature_max=feature_max,
            target_min=target_min,
            target_max=target_max,
            target_names_mask=target_names_mask,
            GB_scale_length=GB_scale_length,
            descale_output=descale_output,
            debias_output=debias_output,
            descale_output_together=descale_output_together,
        )

    @classmethod
    def from_hdf5(
        cls,
        model_file,
        standardization_file,
        nn_type,
        GB_scale_length=1.0,
        descale_output=True,
        debias_output=False,
        descale_output_together=False,
    ):
        model = load_model(model_file, custom_objects={"rmse": rmse, "tf": tf, "ke": ke})
        return cls.from_model(
            model,
            standardization_file,
            nn_type,
            GB_scale_length=GB_scale_length,
            descale_output=descale_output,
            debias_output=debias_output,
            descale_output_together=descale_output_together,
        )

    @classmethod
    def from_json(
        cls,
        model_path,
        weights_path,
        standardization_file,
        nn_type,
        GB_scale_length=1.0,
        descale_output=True,
        debias_output=False,
        descale_output_together=False,
    ):
        with open(model_path, "r") as file:
            lines = file.readlines()
        model = model_from_json("".join(lines), custom_objects={"rmse": rmse, "tf": tf, "ke": ke})
        with open(weights_path, "r") as file:
            weight_dict = json.load(file)
        for layer in model.layers:
            layer.set_weights([np.array(el) for el in weight_dict[layer.name]])
        return cls.from_model(
            model,
            standardization_file,
            nn_type,
            GB_scale_length=GB_scale_length,
            descale_output=descale_output,
            debias_output=debias_output,
            descale_output_together=descale_output_together,
        )

    @classmethod
    def from_model(
        cls,
        model,
        standardization_file,
        nn_type,
        GB_scale_length=1.0,
        descale_output=True,
        debias_output=False,
        descale_output_together=False,
    ):
        stds = pd.read_csv(standardization_file)
        if nn_type == "ETG":
            target_names = pd.Series(["efeETG_GB"])
            branch1_names = ["Ati", "An", "q", "smag", "x", "Ti_Te"]
            branch2_names = ["Ate"]
        elif nn_type == "ITG":
            target_names = pd.Series(["efeITG_GB", "pfeITG_GB", "dfeITG_GB"])
            branch1_names = ["Ate", "An", "q", "smag", "x", "Ti_Te"]
            branch2_names = ["Ati"]
        elif nn_type == "TEM":
            target_names = pd.Series(["efeTEM_GB", "pfeTEM_GB", "dfeTEM_GB"])
            branch1_names = ["Ati", "An", "q", "smag", "x", "Ti_Te"]
            branch2_names = ["Ate"]
        else:
            target_names = pd.Series([])
            branch1_names = []
            branch2_names = []
            print("Choose either ETG, ITG or TEM!!!")
        feature_names = pd.Series(branch1_names + branch2_names)
        stds.set_index("name", inplace=True)
        # Was normalised to s=1, m=0
        s_t = 1
        m_t = 0
        s_sf = stds.loc[feature_names, "std"]
        s_st = stds.loc[target_names, "std"]
        m_sf = stds.loc[feature_names, "mean"]
        m_st = stds.loc[target_names, "mean"]
        feature_scale_factor = s_t / s_sf
        feature_scale_bias = -m_sf * s_t / s_sf + m_t
        target_scale_factor = s_t / s_st
        target_scale_bias = -m_st * s_t / s_st + m_t
        return cls(
            model,
            branch1_names,
            branch2_names,
            feature_names,
            target_names,
            feature_scale_factor,
            feature_scale_bias,
            target_scale_factor,
            target_scale_bias,
            GB_scale_length=GB_scale_length,
            descale_output=descale_output,
            debias_output=debias_output,
            descale_output_together=descale_output_together,
        )

    def get_output(
        self,
        inp,
        clip_low=False,
        clip_high=False,
        low_bound=None,
        high_bound=None,
        safe=True,
        output_pandas=True,
        shift_output_by=0,
        layer_names=None,
    ):
        output = super().get_output(
            inp,
            clip_low=clip_low,
            clip_high=clip_high,
            low_bound=low_bound,
            high_bound=high_bound,
            safe=safe,
            output_pandas=output_pandas,
            shift_output_by=shift_output_by,
            layer_names=layer_names,
        )
        return output

    @classmethod
    def from_files(
        cls,
        model_path,
        standardization_file,
        nn_type,
        GB_scale_length=1.0,
        descale_output=True,
        debias_output=False,
        descale_output_together=False,
    ):
        warnings.warn("from_files is deprecated. Use from_hdf5 instead", DeprecationWarning)
        return cls.from_hdf5(
            model_path,
            standardization_file,
            nn_type,
            GB_scale_length=GB_scale_length,
            descale_output=descale_output,
            debias_output=debias_output,
            descale_output_together=descale_output_together,
        )


class Philipp9DNN(Philipp7DNN):
    @classmethod
    def from_model(
        cls,
        model,
        standardization_file,
        nn_type,
        GB_scale_length=1.0,
        descale_output=True,
        debias_output=False,
        descale_output_together=False,
    ):
        stds = pd.read_csv(standardization_file)
        if nn_type == "ETG":
            target_names = pd.Series(["efeETG_GB"])
            branch1_names = [
                "Zeff",
                "Ati",
                "An",
                "q",
                "smag",
                "x",
                "Ti_Te",
                "logNustar",
            ]
            branch2_names = ["Ate"]
        elif nn_type == "ITG":
            target_names = pd.Series(["efeITG_GB", "efiITG_GB", "pfeITG_GB"])
            branch1_names = [
                "Zeff",
                "Ate",
                "An",
                "q",
                "smag",
                "x",
                "Ti_Te",
                "logNustar",
            ]
            branch2_names = ["Ati"]
        elif nn_type == "TEM":
            target_names = pd.Series(["efeTEM_GB", "efiTEM_GB", "pfeTEM_GB"])
            branch1_names = [
                "Zeff",
                "Ati",
                "An",
                "q",
                "smag",
                "x",
                "Ti_Te",
                "logNustar",
            ]
            branch2_names = ["Ate"]
        else:
            target_names = pd.Series([])
            branch1_names = []
            branch2_names = []
            print("Choose either ETG, ITG or TEM!!!")
        feature_names = pd.Series(branch1_names + branch2_names)
        stds.set_index("name", inplace=True)
        # Was normalised to s=1, m=0
        s_t = 1
        m_t = 0
        s_sf = stds.loc[feature_names, "std"]
        s_st = stds.loc[target_names, "std"]
        m_sf = stds.loc[feature_names, "mean"]
        m_st = stds.loc[target_names, "mean"]
        feature_scale_factor = s_t / s_sf
        feature_scale_bias = -m_sf * s_t / s_sf + m_t
        target_scale_factor = s_t / s_st
        target_scale_bias = -m_st * s_t / s_st + m_t
        return cls(
            model,
            branch1_names,
            branch2_names,
            feature_names,
            target_names,
            feature_scale_factor,
            feature_scale_bias,
            target_scale_factor,
            target_scale_bias,
            GB_scale_length=GB_scale_length,
            descale_output=descale_output,
            debias_output=debias_output,
            descale_output_together=descale_output_together,
        )


class Philipp7DFFNN(KerasNDNN):
    def __init__(
        self,
        model,
        feature_names,
        target_names,
        feature_prescale_factor,
        feature_prescale_bias,
        target_prescale_factor,
        target_prescale_bias,
        feature_min=None,
        feature_max=None,
        target_min=None,
        target_max=None,
        target_names_mask=None,
        GB_scale_length=1.0,
        descale_output=True,
        debias_output=True,
        descale_output_together=False,
    ):
        self._GB_scale_length = GB_scale_length
        self._descale_output_together = descale_output_together
        super().__init__(
            model,
            feature_names,
            target_names,
            feature_prescale_factor,
            feature_prescale_bias,
            target_prescale_factor,
            target_prescale_bias,
            feature_min=feature_min,
            feature_max=feature_max,
            target_min=target_min,
            target_max=target_max,
            target_names_mask=target_names_mask,
            descale_output=descale_output,
            debias_output=debias_output,
        )

    def get_output(
        self,
        inp,
        clip_low=False,
        clip_high=False,
        low_bound=None,
        high_bound=None,
        safe=True,
        output_pandas=True,
    ):
        """
        This should accept a pandas dataframe, and should return a pandas dataframe
        """
        nn_input, safe, clip_low, clip_high, low_bound, high_bound = determine_settings(
            self, inp, safe, clip_low, clip_high, low_bound, high_bound
        )

        nn_input = _prescale(
            nn_input,
            self._feature_prescale_factor.values,
            self._feature_prescale_bias.values,
        )

        # Apply all NN layers
        nn_out = self.model.predict(nn_input)  # Get prediction
        if isinstance(nn_out, np.ndarray):
            output = [nn_out]
        else:
            output = nn_out

        length = output[0].size
        scale_mask = [
            not any(prefix in name for prefix in ["df", "chie", "xaxis"])
            for name in self._target_names
        ]
        for i in range(self._target_names.size):
            if self._debias_output:
                output[i] -= self._target_prescale_bias.iloc[i]
            if self._descale_output:
                if self._descale_output_together:
                    output[i] *= self._target_prescale_factor.apply(lambda x: 1 / x).mean()
                else:
                    output[i] /= self._target_prescale_factor.iloc[i]
            output[i] = output[i].reshape(
                length,
            )
            if self._GB_scale_length != 1.0 and scale_mask[i]:
                output[i] /= self._GB_scale_length

        if isinstance(output, list):
            output = np.stack(output).T
        else:
            output = output[:, np.newaxis]
        output = clip_to_bounds(output, clip_low, clip_high, low_bound, high_bound)

        if output_pandas:
            output = pd.DataFrame(output, columns=self._target_names)

        if self._target_names_mask is not None:
            output.columns = self._target_names_mask
        return output

    @classmethod
    def from_json(
        cls,
        model_path,
        weights_path,
        standardization_file,
        nn_type,
        GB_scale_length=1.0,
        descale_output=True,
        debias_output=False,
        descale_output_together=False,
    ):
        with open(model_path, "r") as file:
            lines = file.readlines()
        model = model_from_json("".join(lines), custom_objects={"rmse": rmse, "tf": tf, "ke": ke})
        with open(weights_path, "r") as file:
            weight_dict = json.load(file)
        for layer in model.layers:
            layer.set_weights([np.array(el) for el in weight_dict[layer.name]])
        return cls.from_model(
            model,
            standardization_file,
            nn_type,
            GB_scale_length=GB_scale_length,
            descale_output=descale_output,
            debias_output=debias_output,
            descale_output_together=descale_output_together,
        )

    @classmethod
    def from_model(
        cls,
        model,
        standardization_file,
        nn_type,
        GB_scale_length=1.0,
        descale_output=True,
        debias_output=False,
        descale_output_together=False,
    ):
        stds = pd.read_csv(standardization_file)
        if nn_type == "ETG":
            target_names = pd.Series(["efeETG_GB"])
        elif nn_type == "ITG":
            target_names = pd.Series(["efeITG_GB", "efiITG_GB", "pfeITG_GB"])
        elif nn_type == "TEM":
            target_names = pd.Series(["efeTEM_GB", "efiTEM_GB", "pfeTEM_GB"])
        else:
            target_names = pd.Series([])
            print("Choose either ETG, ITG or TEM!!!")
        feature_names = pd.Series(["Ati", "Ate", "An", "q", "smag", "x", "Ti_Te"])
        stds.set_index("name", inplace=True)
        # Was normalised to s=1, m=0
        s_t = 1
        m_t = 0
        s_sf = stds.loc[feature_names, "std"]
        s_st = stds.loc[target_names, "std"]
        m_sf = stds.loc[feature_names, "mean"]
        m_st = stds.loc[target_names, "mean"]
        feature_scale_factor = s_t / s_sf
        feature_scale_bias = -m_sf * s_t / s_sf + m_t
        target_scale_factor = s_t / s_st
        target_scale_bias = -m_st * s_t / s_st + m_t
        return cls(
            model,
            feature_names,
            target_names,
            feature_scale_factor,
            feature_scale_bias,
            target_scale_factor,
            target_scale_bias,
            GB_scale_length=GB_scale_length,
            descale_output=descale_output,
            debias_output=debias_output,
            descale_output_together=descale_output_together,
        )


class Daniel7DNN(Philipp7DNN):
    def __init__(
        self,
        model,
        feature_names,
        target_names,
        feature_prescale_factor,
        feature_prescale_bias,
        target_prescale_factor,
        target_prescale_bias,
        feature_min=None,
        feature_max=None,
        target_min=None,
        target_max=None,
        target_names_mask=None,
    ):
        super().__init__(
            model,
            feature_names,
            target_names,
            feature_prescale_factor,
            feature_prescale_bias,
            target_prescale_factor,
            target_prescale_bias,
            feature_min=feature_min,
            feature_max=feature_max,
            target_min=target_min,
            target_max=target_max,
            target_names_mask=target_names_mask,
        )
        self.shift = self.find_shift()

    def get_output(
        self,
        inp,
        clip_low=False,
        clip_high=False,
        low_bound=None,
        high_bound=None,
        safe=True,
        output_pandas=True,
        shift_output=True,
    ):
        if shift_output:
            shift_output_by = self.shift
        else:
            shift_output_by = 0
        output = super().get_output(
            inp,
            clip_low=clip_low,
            clip_high=clip_high,
            low_bound=low_bound,
            high_bound=high_bound,
            safe=safe,
            output_pandas=output_pandas,
            shift_output_by=shift_output_by,
        )
        return output

    def find_shift(self):
        # Define a point where the relu is probably 0
        nn_input = pd.DataFrame(
            {
                "Ati": 0,
                "An": 0,
                "q": 3,
                "smag": 3.5,
                "x": 0.69,
                "Ti_Te": 1,
                "Ate": -100,
            },
            index=[0],
        )
        branched_in = [
            nn_input.loc[:, self._branch1_names].values,
            nn_input.loc[:, self._branch2_names].values,
        ]
        # Get a function to evaluate the network up until the relu layer
        try:
            func = K.function(self.model.input, [self.model.get_layer("TR").output])
        except ValueError:
            raise Exception("'TR' layer not defined, shifting only relevant for new-style NNs")
        relu_out = func(branched_in)
        if relu_out[0][0, 0] != 0:
            raise Exception("Relu is not zero at presumed stable point! Cannot find shift")
        nn_out = self.model.predict(branched_in)
        output = (nn_out - np.atleast_2d(self._target_prescale_bias)) / np.atleast_2d(
            self._target_prescale_factor
        )
        shift = output[0][0]
        return shift


def hdf5_model_to_json(model_file, in_path=None):
    root, ext = os.path.splitext(model_file)
    dirname, base = os.path.split(root)
    if in_path is None:
        in_path = dirname
    model_path = os.path.join(in_path, base + "_model.json")
    weights_path = os.path.join(in_path, base + "_weights.json")

    model = load_model(model_file, custom_objects={"rmse": rmse, "tf": tf, "ke": ke})

    js = model.to_json(indent=2)
    with open(model_path, "w") as file:
        file.write(js)

    weights_list = model.get_weights()
    weight_dict = {}
    for layer in model.layers:
        weight_dict[layer.name] = [arr.tolist() for arr in layer.get_weights()]
    with open(weights_path, "w") as file:
        json.dump(weight_dict, file, indent=2)


output_prefix = "/output"


def calculate_standardization(dataset_path, calc_standardization_on_nonzero=True, columns=None):
    store = pd.HDFStore(dataset_path, "r")
    if columns is None:
        columns = []
        for node_name in store:
            if node_name.startswith(output_prefix):
                columns.append(node_name[len(output_prefix) + 1 :])

    inp = store["/input"]
    df = inp.mean().to_frame("mean").join(inp.std().to_frame("std"))
    for col in columns:
        var = store[output_prefix + "/" + col]
        if calc_standardization_on_nonzero:
            var = var[var != 0]
        df.loc[col, :] = (var.mean(), var.std())

    df.index.name = "name"
    return df


def create_standardization_file(
    dataset_path, target_path, calc_standardization_on_nonzero=True, columns=None
):
    df = calculate_standardization(
        dataset_path,
        calc_standardization_on_nonzero=calc_standardization_on_nonzero,
        columns=columns,
    )
    df.to_csv(target_path)


if __name__ == "__main__":
    # Test the function
    # nn = Daniel7DNN.from_files('../../../IPP-Neural-Networks/Saved-Networks/2018-11-25_Run0161a.h5', 'standardizations_training.csv')
    # shift = nn.find_shift()
    nn = Philipp7DNN.from_files(
        "../../tests/keras_test_files/philippstyle_CGNN_tf1.h5",
        "../../tests/keras_test_files/training_gen3_7D_nions0_flat_filter8.csv",
        "ITG",
        GB_scale_length=3.0,
        debias_output=False,
        descale_output_together=False,
    )
    # create_standardization_file('/mnt/data/qlk_data/pedformreg7/training_gen5_6D_pedformreg7_filter14.h5.1', 'training_gen5_6D_pedformreg7_filter14.csv', calc_standardization_on_nonzero=True)
    # nn = MichaelNN.from_hdf5('10-14-45_16-10-19.hdf5', 'training_gen5_6D_pedformreg7_filter14.csv', ['efeETG_GB'], descale_output=False, debias_output=False)

    scann = 200
    inp = pd.DataFrame()
    inp["Ate"] = np.array(np.linspace(0, 14, scann))
    inp["Ti_Te"] = np.full_like(inp["Ate"], 1.33)
    inp["An"] = np.full_like(inp["Ate"], 3.0)
    inp["Ati"] = np.full_like(inp["Ate"], 5.75)
    inp["q"] = np.full_like(inp["Ate"], 3)
    inp["smag"] = np.full_like(inp["Ate"], 0.7)
    inp["x"] = np.full_like(inp["Ate"], 0.45)
    inp["logNustar"] = np.full_like(inp["Ate"], -3)
    inp["Zeff"] = np.full_like(inp["Ate"], 1)
    inp["At"] = inp["Ate"]
    inp = inp[nn._feature_names]

    fluxes = nn.get_output(inp)
    print(fluxes)
    embed()
