#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import os
import sys
from warnings import warn
from collections import OrderedDict

import numpy as np
import pandas as pd
from IPython import embed

# this_dir = os.path.realpath(os.path.join(__file__, '..'))
# sys.path.append(this_dir)
from qlknn.models.ffnn import clip_to_bounds, determine_settings
import qlknn.models.QLKNNFORT as QLKNNFORT

# sys.path.remove(this_dir)

qlknn_9D_feature_names = [
    "Zeff",
    "Ati",
    "Ate",
    "An",
    "q",
    "smag",
    "x",
    "Ti_Te",
    "logNustar",
]

qlknn_9D_target_names = [
    "efe_GB",
    "efeETG_GB",
    "efi_GB",
    "pfe_GB",
    "dfe_GB",
    "vte_GB",
    "vce_GB",
    "dfi_GB",
    "vti_GB",
    "vci_GB",
]

qlknn_9D_non_merged_target_names = [
    "efeETG_GB",
    "efeITG_GB",
    "efeTEM_GB",
    "efiITG_GB",
    "efiTEM_GB",
    "pfeITG_GB",
    "pfeTEM_GB",
    "dfeITG_GB",
    "dfeTEM_GB",
    "vteITG_GB",
    "vteTEM_GB",
    "vceITG_GB",
    "vceTEM_GB",
    "dfiITG_GB",
    "dfiTEM_GB",
    "vtiITG_GB",
    "vtiTEM_GB",
    "vciITG_GB",
    "vciTEM_GB",
    "gam_leq_GB",
]


class QuaLiKizFortranNN:
    @property
    def _target_names(self):
        if self.opts.merge_modes:
            target_names = self._merged_target_names
        else:
            target_names = self._non_merged_target_names
        return target_names

    @property
    def _feature_min(self):
        return pd.Series(self.opts.min_input, index=self._feature_names)

    @property
    def _feature_max(self):
        return pd.Series(self.opts.max_input, index=self._feature_names)

    @property
    def _target_min(self):
        if self.opts.merge_modes:
            min_target = []
            for var in self._merged_target_names:
                if var in self._non_merged_target_names:
                    idx = self._non_merged_target_names.index(var)
                    min_target.append(self.opts.min_output[idx])
                else:
                    prefix = var[:3]
                    idx = [
                        self._non_merged_target_names.index(name)
                        for name in self._non_merged_target_names
                        if name.startswith(prefix)
                    ]
                    min_target.append(np.sum(self.opts.min_output[idx]))
            return pd.Series(min_target, index=self._target_names)
        else:
            return pd.Series(self.opts.min_output, index=self._target_names)

    @property
    def _target_max(self):
        if self.opts.merge_modes:
            max_target = []
            for var in self._merged_target_names:
                if var in self._non_merged_target_names:
                    idx = self._non_merged_target_names.index(var)
                    max_target.append(self.opts.max_output[idx])
                else:
                    prefix = var[:3]
                    idx = [
                        self._non_merged_target_names.index(name)
                        for name in qlknn_9D_non_merged_target_names
                        if name.startswith(prefix)
                    ]
                    max_target.append(np.sum(self.opts.max_output[idx]))
            return pd.Series(max_target, index=self._target_names)
        else:
            return pd.Series(self.opts.max_output, index=self._target_names)


class QuaLiKizFortranHyperNN(QuaLiKizFortranNN):
    def __init__(self, namelist_path, target_names_mask=None):
        """The QuaLiKiz network embedded in JETTO"""
        self._feature_names = pd.Series(qlknn_9D_feature_names + ["gammaE_QLK", "Te"])
        self.namelist_path = namelist_path
        opts = QLKNNFORT.Qlknn_Types.default_qlknn_hyper_options()
        opts.merge_modes = False
        self.opts = opts

        self._clip_bounds = False

        self._target_names_mask = target_names_mask
        self._merged_target_names = qlknn_9D_target_names
        self._non_merged_target_names = qlknn_9D_non_merged_target_names

    def get_output(
        self,
        input,
        clip_low=False,
        clip_high=False,
        low_bound=None,
        high_bound=None,
        safe=True,
        output_pandas=True,
        verbosity=0,
        R0=None,
        a=None,
        A1=None,
    ):
        """Calculate the output given a specific input

        This function accepts inputs in the form of a dict with
        as keys the name of the specific input variable (usually
        at least the feature_names) and as values 1xN same-length
        arrays.
        """
        nn_input, safe, clip_low, clip_high, low_bound, high_bound = determine_settings(
            self, input, safe, clip_low, clip_high, low_bound, high_bound
        )

        if self.opts.apply_victor_rule:
            if R0 is None or a is None or A1 is None:
                raise TypeError("R0, a, and A1 should be specified if victor rule is applied")
            nrho = input.shape[0]
            if nrho != A1.shape[0]:
                raise ValueError(
                    "A1 should be same shape as norm_input. {!s} != {!s}".format(
                        nrho, A1.shape[0]
                    )
                )
            normpars = QLKNNFORT.Qlknn_Types.Qlknn_Normpars(nrho)
            normpars.a1 = A1
            normpars.a = a
            normpars.r0 = R0
        else:
            normpars = None

        inp_fort = np.asfortranarray(nn_input).T
        if self.opts.merge_modes:
            n_out = 10
        else:
            n_out = 20
        outp_fort = np.asfortranarray(np.full((inp_fort.shape[1], n_out), np.nan))
        # _QLKNNFORT.f90wrap_evaluate_qlknn_10d_direct(self.namelist_path, inp_fort, outp_fort)
        QLKNNFORT.qlknn_python.evaluate_qlknn_10d_direct(
            self.namelist_path,
            inp_fort,
            outp_fort,
            verbosityin=verbosity,
            optsin=self.opts,
            qlknn_normsin=normpars,
        )

        if not self.opts.merge_modes:
            net_evaluate = np.asfortranarray(np.full(20, 0, dtype="int32"))
            rotdiv_evaluate = np.asfortranarray(np.full(19, 0, dtype="int32"))
            QLKNNFORT.qlknn_types.get_networks_to_evaluate(self.opts, net_evaluate)
            outp_fort[:, net_evaluate == 0] = np.NaN
        output = clip_to_bounds(outp_fort, clip_low, clip_high, low_bound, high_bound)

        if output_pandas:
            output = pd.DataFrame(output, columns=self._target_names)

        if self._target_names_mask is not None:
            output.columns = self._target_names_mask
        return output


class QuaLiKizFortranFusionNN(QuaLiKizFortranNN):
    def __init__(self, namelist_path, target_names_mask=None):
        """The QuaLiKiz network embedded in JETTO"""
        self._feature_names = pd.Series(qlknn_9D_feature_names + ["gammaE_QLK", "Te"])
        self.namelist_path = namelist_path
        opts = QLKNNFORT.Qlknn_Types.default_qlknn_fusion_options()
        opts.merge_modes = False
        self.opts = opts

        self._clip_bounds = False

        self._target_names_mask = target_names_mask
        self._non_merged_target_names = [
            "efeETG_GB",
            "efeITG_GB",
            "efeTEM_GB",
            "efiITG_GB",
            "efiTEM_GB",
            "pfeITG_GB",
            "pfeTEM_GB",
        ]
        self._merged_target_names = ["efe_GB", "efeETG_GB", "efi_GB", "pfe_GB"]

    def get_output(
        self,
        input,
        clip_low=False,
        clip_high=False,
        low_bound=None,
        high_bound=None,
        safe=True,
        output_pandas=True,
        verbosity=0,
        R0=None,
        a=None,
        A1=None,
    ):
        """Calculate the output given a specific input

        This function accepts inputs in the form of a dict with
        as keys the name of the specific input variable (usually
        at least the feature_names) and as values 1xN same-length
        arrays.
        """
        nn_input, safe, clip_low, clip_high, low_bound, high_bound = determine_settings(
            self, input, safe, clip_low, clip_high, low_bound, high_bound
        )

        if self.opts.apply_victor_rule:
            ValueError("Fusion NN cannot be run with victor rule")
        else:
            normpars = None

        inp_fort = np.asfortranarray(nn_input).T
        if self.opts.merge_modes:
            n_out = 4
        else:
            n_out = 7
        outp_fort = np.asfortranarray(np.full((inp_fort.shape[1], n_out), np.nan))
        # _QLKNNFORT.f90wrap_evaluate_qlknn_10d_direct(self.namelist_path, inp_fort, outp_fort)
        QLKNNFORT.qlknn_python.evaluate_qlknn_fusion_direct(
            self.namelist_path,
            inp_fort,
            outp_fort,
            verbosityin=verbosity,
            optsin=self.opts,
            qlknn_normsin=normpars,
        )

        output = clip_to_bounds(outp_fort, clip_low, clip_high, low_bound, high_bound)

        if output_pandas:
            output = pd.DataFrame(output, columns=self._target_names)

        if self._target_names_mask is not None:
            output.columns = self._target_names_mask
        return output


if __name__ == "__main__":
    # Test the function
    root = os.path.dirname(os.path.realpath(__file__))
    nn = QuaLiKizFortranHyperNN(
        os.path.join(root, "../../../QLKNN-fortran/lib/src/qlknn-hyper-namelists")
    )

    scann = 24
    input = pd.DataFrame()
    input["Ati"] = np.array(np.linspace(2, 13, scann))
    input["Ti_Te"] = np.full_like(input["Ati"], 1.0)
    input["Te"] = np.full_like(input["Ati"], 1.0)
    input["Zeff"] = np.full_like(input["Ati"], 1.0)
    input["An"] = np.full_like(input["Ati"], 2.0)
    input["Ate"] = np.full_like(input["Ati"], 5.0)
    input["q"] = np.full_like(input["Ati"], 0.660156)
    input["smag"] = np.full_like(input["Ati"], 0.399902)
    input["Nustar"] = np.full_like(input["Ati"], 0.009995)
    input["x"] = np.full_like(input["Ati"], 0.449951)
    input["logNustar"] = np.full_like(input["Ati"], np.log10(input["Nustar"]))
    input["Zeff"] = np.full_like(input["Ati"], 1)
    input["Machtor"] = np.full_like(input["Ati"], 0.3)
    input["gammaE_QLK"] = np.full_like(input["Ati"], -0.1)
    input = input[nn._feature_names]

    fluxes = nn.get_output(input)
    print(fluxes)

    print("Fusion NN")
    fusion_nn = QuaLiKizFortranFusionNN(
        os.path.join(root, "../../../QLKNN-fortran/lib/src/qlknn-fusion-namelists")
    )
    input = input[fusion_nn._feature_names]
    fluxes = fusion_nn.get_output(input)
    print(fluxes)
