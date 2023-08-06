# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/MrCode403/Jarves/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyJarvis/blob/main/LICENSE>.

"""
Exceptions which can be raised by py-Ultroid Itself.
"""


class pyJarvisError(Exception):
    ...


class TelethonMissingError(ImportError):
    ...


class DependencyMissingError(ImportError):
    ...


class RunningAsFunctionLibError(pyJarvisError):
    ...
