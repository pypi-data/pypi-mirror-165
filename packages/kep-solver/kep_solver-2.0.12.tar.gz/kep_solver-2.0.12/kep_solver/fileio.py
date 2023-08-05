"""This module contains file IO functions."""

import json
import typing
from defusedxml import ElementTree as ET  # type: ignore

from kep_solver.entities import Instance, Donor, Transplant
from kep_solver.model import Model, UK_age_score
from kep_solver.pool import Pool, Solution
from kep_solver.graph import Exchange


def read_json(filename: str) -> Instance:
    """Read an instance in JSON format from the given file

    :param filename: The name of the file containing the JSON instance
    :return: the corresponding Instance
    """
    with open(filename, "r") as infile:
        return parse_json(infile.read())


def parse_json(jsonstring: str) -> Instance:
    """Read an instance in JSON format from the given string

    :param jsonstring: A string holding a JSON representation of
        the instance
    :return: the corresponding Instance
    """
    json_obj = json.loads(jsonstring)
    instance = Instance()
    data = json_obj["data"]
    for donor_id, donor_data in data.items():
        donor = Donor(donor_id)
        if "dage" in donor_data:
            donor.age = float(donor_data["dage"])
        if "bloodtype" in donor_data:
            donor.bloodGroup = donor_data["bloodtype"]
        if "sources" not in donor_data:
            donor.NDD = True
        elif len(donor_data["sources"]) == 0:
            donor.NDD = True
        elif len(donor_data["sources"]) != 1:
            raise Exception("Donor with more than one recipient detected")
        else:
            recip = instance.recipient(str(donor_data["sources"][0]))
            donor.recipient = recip
            recip.addDonor(donor)
        instance.addDonor(donor)
        if "matches" in donor_data:
            for arc in donor_data["matches"]:
                recip = instance.recipient(str(arc["recipient"]))
                t = Transplant(donor, recip, float(arc["score"]))
                instance.addTransplant(t)
    if "recipients" in json_obj:
        recips = json_obj["recipients"]
        for rid, info in recips.items():
            recip = instance.recipient(str(rid))
            if "pra" in info:
                recip.cPRA = float(info["pra"])
            if "cPRA" in info:
                recip.cPRA = float(info["cPRA"])
            if "bloodgroup" in info:
                recip.bloodGroup = info["bloodgroup"]
            if "bloodtype" in info:
                recip.bloodGroup = info["bloodtype"]
    return instance


def read_xml(filename: str) -> Instance:
    """Read an instance in XML format from the given file

    :param filename: The name of the file containing the XML instance
    :return: the corresponding Instance
    """
    with open(filename, "r") as infile:
        return parse_xml(infile.read())


def parse_xml(xmlstring: str) -> Instance:
    """Read an instance in XML format from the given string

    :param xmlstring: A string holding a XML representation of
        the instance
    :return: the corresponding Instance
    """
    xml = ET.fromstring(xmlstring)
    instance = Instance()
    for donor_xml in xml:
        donor = Donor(donor_xml.attrib["donor_id"])
        age_xml = donor_xml.find("dage")
        if age_xml is not None:
            donor.age = float(age_xml.text)
        bloodgroup_xml = donor_xml.find("bloodgroup")
        if bloodgroup_xml is not None:
            donor.bloodGroup = bloodgroup_xml.text
        sources = donor_xml.find("sources")
        if sources is not None:
            if len(sources) == 0:
                donor.NDD = True
            elif len(sources) != 1:
                raise Exception("Donor with more than one recipient detected")
            recip = instance.recipient(str(sources[0].text))
            donor.recipient = recip
            recip.addDonor(donor)
        else:
            donor.NDD = True
        instance.addDonor(donor)
        matches = donor_xml.find("matches")
        if matches is not None:
            for match in matches:
                recip = instance.recipient(str(match.find("recipient").text))
                score = float(match.find("score").text)
                t = Transplant(donor, recip, score)
                instance.addTransplant(t)
    return instance


def read_file(filename: str) -> Instance:
    """Read a file containing a KEP instance. Will attempt to detect the
    correct file format if possible.

    :param filename: The name of the file containing the instance
    :return: the corresponding Instance
    """
    if filename[-4:] == ".xml":
        return read_xml(filename)
    if filename[-5:] == ".json":
        return read_json(filename)
    raise Exception(f"Unknown filetype: {filename}")


# The UK output format needs "two_way", "three_way" and so-on.
_NUM_TO_WORDS = {
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
}


class UKJson:
    """A class for outputing JSON-formatted results in the style prescribed by
    the UK KEP and NHSBT.
    """

    def __init__(self, model: Model, pool: Pool, solution: Solution):
        self._pool: Pool = pool
        self._model: Model = model
        self._solution: Solution = solution

    def _cycle(self, exchange: Exchange):
        """Create the appropriate JSON object for an exchange."""
        cycles = []
        total_weight = 0
        for ind, vertex in enumerate(exchange):
            donor = vertex.donor
            inner_obj = {"d": donor.id}
            if donor.NDD:
                inner_obj["a"] = True
            else:
                inner_obj["p"] = donor.recipient.id
            target_v = exchange[(ind + 1) % len(exchange)]
            if target_v.donor.NDD:
                inner_obj["tb"] = 0
                inner_obj["dif"] = 0
                inner_obj["s"] = 0
                desired = set([donor.recipient])
            else:
                recipient = target_v.donor.recipient
                bonus, tb = UK_age_score(donor, target_v.donor)
                transplants = [
                    t for t in donor.transplants() if t.recipient == recipient
                ]
                assert len(transplants) == 1
                transplant = transplants[0]
                inner_obj["tb"] = tb
                inner_obj["dif"] = bonus
                inner_obj["s"] = transplant.weight
                total_weight += tb + bonus + transplant.weight
                if donor.NDD:
                    desired = set([recipient])
                else:
                    desired = set([donor.recipient, recipient])
            if len(exchange) == 3:
                # Search for a backarc only in exchanges with 3 vertices
                best_score = -1
                # If there are multiple potential backarcs, we want the one
                # with the best score
                for backarc in exchange.backarc_exchanges_uk():
                    if set(backarc.all_recipients()) == desired:
                        if len(backarc) == 2:  # 2 vertices in the "backarc exchange"
                            new_score = self._model.exchange_values(backarc)[-1]
                            if new_score > best_score:
                                inner_obj["b"] = backarc.id
                                best_score = new_score
            cycles.append(inner_obj)
        obj = {
            "cycle": cycles,
            "backarcs": exchange.num_backarcs_uk(),
            "weight": round(total_weight, 5),
            "alt": [alternate.id for alternate in exchange.alternates],
        }
        return obj

    def to_string(self) -> str:
        """Return a string representing the solution as a JSON object.

        :return: A string representing the JSON.
        """
        obj: dict[str, typing.Any] = {"algorithm": self._pool.description}
        obj["output"] = {
            "all_cycles": {
                modelled.exchange.id: self._cycle(modelled.exchange)
                for modelled in self._solution.possible
                if len(modelled.exchange) >= 2
            }
        }
        obj["exchange_data"] = [
            {
                "description": self._pool.description,
                "exchanges": [
                    modelled.exchange.id for modelled in self._solution.selected
                ],
                "weight": round(self._solution.values[-1], 5),
                "total_transplants": self._solution.values[1],
            }
        ]
        for i in range(
            2, max(self._pool.maxCycleLength, self._pool.maxChainLength) + 1
        ):
            name = f"{_NUM_TO_WORDS[i]}_way_exchanges"
            count = len([c for c in self._solution.selected if len(c.exchange) == i])
            obj["exchange_data"][0][name] = count
        return json.dumps(obj)

    def write(self, output: typing.TextIO):
        """Write the details to a JSON file, or file-like object.

        :param output: A file-like object where output will be written.
        """
        output.write(self.to_string())
