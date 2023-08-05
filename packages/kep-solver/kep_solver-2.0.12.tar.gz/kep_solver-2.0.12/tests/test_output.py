import pytest

import kep_solver.model as model
import kep_solver.pool as pool
import kep_solver.fileio as fileio


@pytest.fixture(scope="module")
def transplant_pool():
    eff = model.EffectiveTwoWay()
    max_size = model.TransplantCount()
    backarcs = model.BackArcs()
    threes = model.ThreeWay()
    score = model.UKScore()
    objectives = [eff, max_size, threes, backarcs, score]
    return pool.Pool(
        objectives,
        description="UKLKSS Optimal set of exchanges",
        maxCycleLength=3,
        maxChainLength=3,
    )


def test_transplant_count_test1(transplant_pool):
    instance = fileio.read_json("tests/test_instances/test1.json")
    solution, model = transplant_pool.solve_single(instance)
    json_obj = fileio.UKJson(model, transplant_pool, solution)
    output = json_obj.to_string()
    with open("tests/test_instances/test1_output.json", "r") as infile:
        expected = infile.read().rstrip()
    assert output == expected


def test_transplant_count_test9(transplant_pool):
    instance = fileio.read_json("tests/test_instances/test9.json")
    solution, model = transplant_pool.solve_single(instance)
    json_obj = fileio.UKJson(model, transplant_pool, solution)
    output = json_obj.to_string()
    with open("tests/test_instances/test9_output.json", "r") as infile:
        expected = infile.read().rstrip()
    assert output == expected


def test_transplant_count_test10(transplant_pool):
    instance = fileio.read_json("tests/test_instances/test10.json")
    solution, model = transplant_pool.solve_single(instance)
    json_obj = fileio.UKJson(model, transplant_pool, solution)
    output = json_obj.to_string()
    with open("tests/test_instances/test10_output.json", "r") as infile:
        expected = infile.read().rstrip()
    assert output == expected
