from __future__ import annotations

import logging
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Union

from pyteomics import mzid

from psm_utils.io._base_classes import ReaderBase, WriterBase
from psm_utils.io.exceptions import PSMUtilsIOException
from psm_utils.peptidoform import Peptidoform
from psm_utils.psm import PeptideSpectrumMatch
from psm_utils.psm_list import PSMList

logger = logging.getLogger(__name__)

STANDARD_SEARCHENGINE_SCORES = [
    "Amanda:AmandaScore",
    "Andromeda:score",
    "Byonic:Score",
    "Comet:Xcorr",
    "DeBunker:score",
    "IdentityE Score",
    "KSDP score",
    "MS-GF:RawScore",
    "MSFit:Mowse score",
    "MSPathFinder:RawScore" "MSPepSearch:score",
    "Mascot:score",
    "MetaMorpheus:score",
    "OMSSA:evalue",
    "OpenPepXL:score",
    "PEAKS:peptideScore",
    "PeptideShaker PSM score",
    "Phenyx:Pepzscore",
    "ProLuCID:xcorr",
    "ProSight:specral C-score",
    "Profound:z value",
    "ProteinProspector:score",
    "ProteinScape:SequestMetaScore",
    "ProteomeDiscoverer:Delta Score",
    "SEQUEST:xcorr",
    "SIM-XL score ",
    "SQID:score ",
    "Sonar:Score",
    "SpectrumMill:Score",
    "TopMG:spectral E-Value",
    "X!Tandem:hyperscore",
    "ZCore:probScore:",
    "Percolator:scrolledtext",
    "xi:score",
]


class MzidReader(ReaderBase):
    def __init__(self, filename: Union[str, Path], *args, **kwargs) -> None:

        """
        Reader for MZID Record PSM files.

        Parameters
        ----------
        filename: str, pathlib.Path
            Path to PSM file.

        Examples
        --------

        MzidReader supports iteration:

        >>> from psm_utils.io.mzid import MzidReader
        >>> for psm in MzidReader("peptides_1_1_0.mzid"):
        ...     print(psm.peptide.proforma)
        ACDEK
        AC[Carbamidomethyl]DEFGR
        [Acetyl]-AC[Carbamidomethyl]DEFGHIK

        Or a full file can be read at once into a :py:class:`psm_utils.psm_list.PSMList`
        object:

        >>> mzid_reader = MzidReader("peptides_1_1_0.mzid")
        >>> psm_list = mzid_reader.read_file()

        """
        super().__init__(filename, *args, **kwargs)
        self._source = self._infer_source()
        self._searchengine_key_dict = self._get_searchengine_specific_keys()

    def __iter__(self):
        """Iterate over file and return PSMs one-by-one."""
        with mzid.read(str(self.filename)) as reader:
            for spectrum in reader:
                spectrum_title = spectrum[self._searchengine_key_dict["spectrum_key"]]
                raw_file = Path(spectrum["location"]).stem
                for entry in spectrum["SpectrumIdentificationItem"]:
                    psm = self._get_peptide_spectrum_match(
                        spectrum_title, raw_file, entry)
                    yield psm

    def read_file(self) -> PSMList:
        """Read full mzid file to PSM list object."""
        return PSMList(psm_list=[psm for psm in self.__iter__()])

    @staticmethod
    def _get_xml_namespace(root_tag):
        """Get the namespace of the xml root."""
        m = re.match(r"\{.*\}", root_tag)
        return m.group(0) if m else ""

    def _infer_source(self):
        """Get the source of the mzid file."""
        mzid_xml = ET.parse(self.filename)
        root = mzid_xml.getroot()
        name_space = self._get_xml_namespace(root.tag)
        return root.find(f".//{name_space}AnalysisSoftware").attrib["name"]

    def _get_searchengine_specific_keys(self):
        """Get searchengine specific keys."""
        if "PEAKS" in self._source:
            return {
                "score_key": "PEAKS:peptideScore",
                "rt_key": "retention time",
                "spectrum_key": "spectrumID",
            }
        elif self._source == "MS-GF+":
            return {
                "score_key": "MS-GF:RawScore",
                "rt_key": "scan start time",
                "spectrum_key": "spectrum title",
            }
        # if source is not known return standard keys and infer score key
        return {
            "score_key": self._infer_score_name(),
            "rt_key": "retention time",
            "spectrum_key": "spectrumID",
        }

    def _infer_score_name(self) -> str:
        """Infer the score from the known list of PSM scores."""
        with mzid.read(str(self.filename)) as reader:
            for spectrum in reader:
                sii_keys = spectrum["SpectrumIdentificationItem"][0].keys()
                break
        for score in STANDARD_SEARCHENGINE_SCORES:
            if score in sii_keys:
                return score
        else:
            raise UnknownMzidScore("No known score metric found in mzIdentML file.")

    @staticmethod
    def _parse_peptidoform(seq: str, modification_list: list[dict], charge: int):
        """Parse mzid sequence and modifications to Peptidoform."""
        peptide = [""] + list(seq) + [""]

        # Add modification labels
        for mod in modification_list:
            peptide[int(mod["location"])] += f"[{mod['name']}]"

        # Add dashes between residues and termini, and join sequence
        peptide[0] = peptide[0] + "-" if peptide[0] else ""
        peptide[-1] = "-" + peptide[-1] if peptide[-1] else ""
        proforma_seq = "".join(peptide)

        # Add charge state
        proforma_seq += f"/{charge}"

        return Peptidoform(proforma_seq)

    @staticmethod
    def _parse_peptide_evidence_ref(peptide_evidence_list: list[dict]):
        """Parse peptide evidence References of PSM."""
        isdecoy = peptide_evidence_list[0]["isDecoy"]
        protein_list = [
            d["accession"] for d in peptide_evidence_list if "accession" in d.keys()
        ]
        return isdecoy, protein_list

    def _get_searchengine_specific_metadata(self, spectrum_identification_item):
        """Get searchengine specific psm metadata."""
        sii = spectrum_identification_item
        metadata = {
            "calculatedMassToCharge": sii["calculatedMassToCharge"],
            "rank": sii["rank"],
            "length": len(sii["PeptideSequence"]),
        }
        if self._source == "MS-GF+":
            metadata.update({
                "MS-GF:DeNovoScore": sii["MS-GF:DeNovoScore"],
                "MS-GF:EValue": sii["MS-GF:EValue"],
                "MS-GF:DeNovoScore": sii["MS-GF:DeNovoScore"],
                "IsotopeError": sii["IsotopeError"],
            })
        return metadata

    def _get_peptide_spectrum_match(
        self,
        spectrum_title: str,
        raw_file: str,
        spectrum_identification_item: dict[str, Union[str, float, list]],
    ) -> PeptideSpectrumMatch:
        """Parse single mzid entry to :py:class:`~psm_utils.peptidoform.Peptidoform`."""
        sii = spectrum_identification_item

        try:
            modifications = sii["Modification"]
        except KeyError:
            modifications = []
        sequence = sii["PeptideSequence"]
        peptide = self._parse_peptidoform(sequence, modifications, sii["chargeState"])
        is_decoy, protein_list = self._parse_peptide_evidence_ref(
            sii["PeptideEvidenceRef"]
        )
        try:
            rt = float(sii[self._searchengine_key_dict["rt_key"]])
        except KeyError:
            rt = float("nan")

        psm = PeptideSpectrumMatch(
            peptide=peptide,
            spectrum_id=spectrum_title,
            run=raw_file,
            is_decoy=is_decoy,
            score=sii[self._searchengine_key_dict["score_key"]],
            precursor_mz=sii["experimentalMassToCharge"],
            retention_time=rt,
            protein_list=protein_list,
            source=self._source,
            provenance_data={"mzid_filename": str(self.filename)},
            metadata=self._get_searchengine_specific_metadata(sii),
        )
        return psm


class MzidWriter(WriterBase):
    """Writer for MaxQuant msms.txt files (not implemented)."""

    def __init__(self, filename):
        raise NotImplementedError()

    def write_psm(self, psm: PeptideSpectrumMatch):
        """Write a single PSM to the MaxQuant msms.txt PSM file."""
        raise NotImplementedError()

    def write_file(self, psm_list: PSMList):
        """Write entire PSMList to the MaxQuant msms.txt PSM file."""
        raise NotImplementedError()


class UnknownMzidScore(PSMUtilsIOException):
    """Exception while handling or parsing peptide modifications."""

    pass
