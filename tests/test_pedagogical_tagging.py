import json
from pathlib import Path
from projects.ZoteroPDF.scripts.tag_pedagogical import score_text

def test_score_text_positive():
    text = """# Instructional Implications\n\nThis section outlines pedagogical strategies for classroom application.\nTeachers can adapt the instructional strategy to enhance learner engagement and curriculum design.\nConclusion: These teaching implications matter."""
    metrics = score_text(text)
    assert metrics['score'] >= 8
    assert metrics['primary_hits'] >= 2
    assert metrics['heading_hits'] >= 1


def test_score_text_negative():
    text = """# Background\nThis paper describes statistical properties of the algorithm without discussing classrooms or pedagogy."""
    metrics = score_text(text)
    assert metrics['score'] < 8


def test_manifest_integration(tmp_path):
    # build fake manifest
    manifest = {"files": {}}
    doc = tmp_path / "doc.md"
    doc.write_text("Pedagogical teaching practice curriculum design.")
    manifest['files'][str(doc)] = {}
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))

    # run tagging logic inline
    from projects.ZoteroPDF.scripts.tag_pedagogical import score_text
    text = doc.read_text()
    metrics = score_text(text)
    positive = metrics['score'] >= 8
    if positive:
        manifest['files'][str(doc)]['pedagogical_implications'] = True
    assert positive is True
