import pytest as pytest
from IPython import embed  # pylint: disable=unused-import # noqa: F401

from qlknn.models.committee import *


class TestQuaLiKizCommitteeNN:
    def test_initialize(self, efiITG_committee_nets):
        nn_ITG = QuaLiKizCommitteeNN(efiITG_committee_nets)
        assert isinstance(nn_ITG, QuaLiKizCommitteeNN)

    def test_get_output_default(self, efiITG_committee_nets, inp_7D_df):
        nn_ITG = QuaLiKizCommitteeNN(efiITG_committee_nets)
        outp_ITG = nn_ITG.get_output(inp_7D_df)
        assert len(outp_ITG.columns) == 2
        assert len(outp_ITG.index) == 100


class TestQuaLiKizCommitteeProductNN:
    def test_initialize(self, efiITG_committee_nets, efeTEM_committee_nets):
        nn_ITG = QuaLiKizCommitteeNN(efiITG_committee_nets)
        nn_TEM = QuaLiKizCommitteeNN(efeTEM_committee_nets)
        new_name = "efiITG_GB_prod_efeTEM_GB"
        nn = QuaLiKizCommitteeProductNN([new_name, new_name], [nn_ITG, nn_TEM])

    def test_get_output_default(self, efiITG_committee_nets, efeTEM_committee_nets, inp_7D_df):
        nn_ITG = QuaLiKizCommitteeNN(efiITG_committee_nets)
        nn_TEM = QuaLiKizCommitteeNN(efeTEM_committee_nets)
        new_name = "efiITG_GB_prod_efeTEM_GB"
        nn = QuaLiKizCommitteeProductNN([new_name, new_name + "_EB"], [nn_ITG, nn_TEM])
        outp = nn.get_output(inp_7D_df)
        assert len(outp.columns) == 2
        assert len(outp.index) == 100


class TestQuaLiKizNDNNCollection:
    def test_initialize(self, efiITG_committee_nets, efeTEM_committee_nets, inp_7D_df):
        nn_ITG = QuaLiKizCommitteeNN(efiITG_committee_nets)
        nn_TEM = QuaLiKizCommitteeNN(efeTEM_committee_nets)
        nn = QuaLiKizNDNNCollection([nn_ITG, nn_TEM])
        outp = nn.get_output(inp_7D_df)
        assert len(outp.columns) == 4
        assert len(outp.index) == 100
