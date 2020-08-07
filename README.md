# Type.World GUI App


[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/github/typeworld/guiapp?svg=true)](https://ci.appveyor.com/project/typeworld/guiapp)
Compiled versions of this app are available [here](https://type.world/app/).

If you want to run this code directly, you need to install [wxPython](https://wiki.wxpython.org/How%20to%20install%20wxPython) as well as the Python libraries [typeworld](https://github.com/typeworld/api/tree/master/Python/Lib/typeworld) and [ynlib](https://github.com/yanone/ynlib).

# Dependencies

`pip install wxPython babel`

Further:

`pip install modulegraph macholib dmgbuild pystray`

# Translations

If you care about translating Type.World’s user interface, please refrain from adding your translation to the `json` file and then PR-ing it. The translations are maintained in an online collaborative database on [type.world](https://type.world), which isn’t finished yet. Adding translations is slated for the Beta phase which starts end of January 2020.

Instead, please get in touch and I'll note your participation:

* English/German: Yanone
* Spanish: [Adolfo Jayme-Barrientos](https://github.com/fitojb)

# Build

Install "Developer ID Certificate" code signing certificate through XCode -> Account.

# Test

Run compiled app in Python virtual environment to check for missing dependencies.
