from ..models import DataDisclosureAgreementModel


class DDATemplate:
    """To manage DDA template lifecycle"""

    # Create, Read, Update, Deactivate
    # Impact towards Data Disclosure Agreement Instances ?
    # Instances have their own lifecycle as once they are instances
    # They are separated from templates other the fact that there is
    # a reference to a template version.
    # At present, draft templates are those with all mandatory fields
    # filled in, but is not yet ready to be published.
    # It is not possibled to drafted without mandatory
    # fields available.

    def __init__(
        self,
        *,
        dda: DataDisclosureAgreementModel,
        deactivated: bool,
        draft: bool,
    ) -> None:
        """Initialise DDA template"""

        # Set attributes
        self._dda = dda
        self._deactivated = deactivated
        self._draft = draft

    @property
    def dda(self) -> DataDisclosureAgreementModel:
        """Returns Data Disclosure Agreement"""
        return self._dda

    @property
    def deactivated(self) -> bool:
        """Returns if DDA template is deactivated or not"""
        return self._deactivated

    @property
    def draft(self) -> bool:
        """Returns if DDA template is draft or not"""
        return self._draft
