"""Unit tests for the deterministic (non-LLM) part of the matcher tool.
Run with:  pytest tests/
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.tools.matcher_tool import skill_overlap, experience_score


def test_skill_overlap_full_match():
    score, matched, missing = skill_overlap(
        ["Python", "AWS", "Docker"], ["python", "aws", "docker"]
    )
    assert score == 100.0
    assert matched == ["aws", "docker", "python"]
    assert missing == []


def test_skill_overlap_partial_match():
    score, matched, missing = skill_overlap(
        ["Python", "Django"], ["python", "kubernetes", "docker"]
    )
    assert round(score, 2) == round(100 / 3, 2)
    assert matched == ["python"]
    assert set(missing) == {"kubernetes", "docker"}


def test_skill_overlap_no_required_skills():
    score, matched, missing = skill_overlap(["Python"], [])
    assert score == 0.0
    assert matched == []
    assert missing == []


def test_experience_score_meets_requirement():
    assert experience_score(6, 5) == 100.0


def test_experience_score_below_requirement():
    assert experience_score(2.5, 5) == 50.0


def test_experience_score_unknown_experience():
    assert experience_score(None, 5) == 50.0


def test_experience_score_no_requirement():
    assert experience_score(None, None) == 100.0
