import ispyb.model.__future__
import ispyb.model.datacollection
import ispyb.model.samplegroup


def test_dc_no_sample_groups(testdb, testconfig):
    ispyb.model.__future__.enable(testconfig)
    dc = testdb.get_data_collection(1052503)
    assert len(dc.sample_groups) == 0


def test_dc_sample_groups(testdb, testconfig):
    ispyb.model.__future__.enable(testconfig)
    dc = testdb.get_data_collection(1066786)
    assert len(dc.sample_groups) == 2
    for sample_group in dc.sample_groups:
        assert dc.dcid in sample_group.dcids


def test_sample_group_no_linked_dcids(testdb, testconfig):
    ispyb.model.__future__.enable(testconfig)
    sample_group = ispyb.model.samplegroup.SampleGroup(5, testdb)
    assert str(sample_group) == "SampleGroup #5 (not yet loaded from database)"
    sample_group.reload()
    assert sample_group.sample_ids == [398824, 398827]
    assert len(sample_group.dcids) == 0
    assert (
        str(sample_group)
        == """\
SampleGroup #5
  Name       : None
  Sample ids : 398824,398827
  DCIDs      : None\
"""
    )


def test_sample_group_single_sample(testdb, testconfig):
    ispyb.model.__future__.enable(testconfig)
    sample_group = ispyb.model.samplegroup.SampleGroup(6, testdb)
    sample_group.reload()
    assert sample_group.sample_ids == [398810]
    assert sample_group.name == "foo"
    assert sample_group.dcids == [1066786]
    assert (
        str(sample_group)
        == """\
SampleGroup #6
  Name       : foo
  Sample ids : 398810
  DCIDs      : 1066786\
"""
    )


def test_sample_group_linked_dcids(testdb, testconfig):
    ispyb.model.__future__.enable(testconfig)
    sample_group = ispyb.model.samplegroup.SampleGroup(7, testdb)
    sample_group.reload()
    assert sample_group.sample_ids == [374695, 398810]
    assert sample_group.name == "bar"
    assert sample_group.dcids == [993677, 6017405, 1066786]
    assert (
        str(sample_group)
        == """\
SampleGroup #7
  Name       : bar
  Sample ids : 374695,398810
  DCIDs      : 993677,6017405,1066786\
"""
    )


def test_get_sample_group(testdb, testconfig):
    sample_group = testdb.get_sample_group(5)
    assert isinstance(sample_group, ispyb.model.samplegroup.SampleGroup)
    assert sample_group.id == 5
