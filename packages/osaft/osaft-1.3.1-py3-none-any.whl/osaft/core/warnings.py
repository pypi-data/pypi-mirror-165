import warnings

from osaft import log

EPS = 1e-2


class AssumptionWarning(Warning):
    """Warning that the used solution might not be valid based on the set
    material parameters
    """

    pass


def raise_assumption_warning(test: bool, msg: str = '') -> None:
    """ Raises :class:`AssumptionWarning` if :attr:`test` is `True`

    :param test: test that checks for warning
    :param msg: message for more descriptive warning message
    """

    if test:
        message = ('Theory might not be valid anymore!')
        message += msg

        warnings.warn(message, category=AssumptionWarning, stacklevel=5)
        log.info(message)


if __name__ == '__main__':
    pass
