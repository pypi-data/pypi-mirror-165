
from typing import cast

from logging import Logger
from logging import getLogger

from untanglepyut.UnTangler import Documents
from untanglepyut.UnTangler import UnTangler

from oglio.Types import OglActors
from oglio.Types import OglClasses
from oglio.Types import OglDocument
from oglio.Types import OglLinks
from oglio.Types import OglNotes
from oglio.Types import OglProject
from oglio.Types import OglTexts
from oglio.Types import OglUseCases


class Reader:
    """
    This is a simple translation layer on top of the PyutUntangler library.  This
    layer simply hides that implementation detail and provides a more usable
    interface to Pyut.  Additionally, it serves as a common piece of code
    that allows and IOPlugin implementations
    See https://github.com/hasii2011/pyutplugincore
    """
    def __init__(self):

        self.logger: Logger = getLogger(__name__)
        self.logger: Logger = getLogger(__name__)

    def read(self, fqFileName: str) -> OglProject:

        """
        Parse the input XML file

        Args:
            fqFileName: Fully qualified file name
        """
        untangler: UnTangler = UnTangler(fqFileName=fqFileName)

        untangler.untangle()

        oglProject: OglProject = OglProject()

        oglProject.toOglProject(untangler.projectInformation)

        documents: Documents = untangler.documents
        for document in documents.values():
            self.logger.debug(f'Untangled - {document.documentTitle}')
            oglDocument: OglDocument = OglDocument()
            oglDocument.toOglDocument(document)
            #
            # Cheat by just type casting
            #
            oglDocument.oglClasses  = cast(OglClasses,  document.oglClasses)
            oglDocument.oglLinks    = cast(OglLinks,    document.oglLinks)
            oglDocument.oglNotes    = cast(OglNotes,    document.oglNotes)
            oglDocument.oglTexts    = cast(OglTexts,    document.oglTexts)
            oglDocument.oglActors   = cast(OglActors,   document.oglActors)
            oglDocument.oglUseCases = cast(OglUseCases, document.oglUseCases)

            self.logger.debug(f'OglDocument - {oglDocument}')
            oglProject.oglDocuments[oglDocument.documentTitle] = oglDocument

        return oglProject
