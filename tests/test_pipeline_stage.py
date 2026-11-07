import pytest

from streaming_pipeline import PipelineStage


def test_pipeline_stage_is_abstract():
    with pytest.raises(TypeError):
        PipelineStage("Test Stage")