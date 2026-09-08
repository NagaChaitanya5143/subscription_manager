import pathlib


def test_no_hardcoded_api_key():
    text = pathlib.Path("benchmark.py").read_text(encoding="utf-8")
    assert "nvapi-" not in text
    assert "Authorization" not in text or "os.getenv" in text


def test_agent_uses_environment_for_api_key():
    agent_text = pathlib.Path("agent.py").read_text(encoding="utf-8")
    assert "os.getenv(\"NVIDIA_API_KEY\")" in agent_text
    assert "os.getenv(\"OPENAI_API_KEY\")" in agent_text
