from aiogram.fsm.state import State, StatesGroup

class OrderState(StatesGroup):
    #main
    waiting_for_project_type = State()
    waiting_for_category = State()
    waiting_for_po = State()

    #minecraft
    waiting_for_name = State()
    waiting_for_version = State()
    waiting_for_socials = State()
    waiting_for_colors = State()
    waiting_for_mode = State()
    waiting_for_functionality = State()
    waiting_for_spawn = State()
    waiting_for_holograms = State()
    waiting_for_plugins = State()
    waiting_for_launcher = State()
    waiting_for_icon = State()
    waiting_for_donations = State()
    waiting_for_additional = State()
    waiting_for_deadline = State()
    waiting_for_support = State()
    waiting_for_source = State()

    #plugin
    waiting_for_namePlugin = State()
    waiting_for_jarPlugin = State()
    waiting_for_versionPlugin = State()
    waiting_for_funcPlugin = State()
    waiting_for_addonsPlugin = State()
    waiting_for_examplesPlugin = State()
    waiting_for_extraInfoPlugin = State()
    waiting_for_deadlinePlugin = State()
    waiting_for_howDouKnowUsPlugin = State()
    waiting_for_sourcePlugin = State()

    #launcher
    waiting_for_nameLauncher = State()
    waiting_for_versionLauncher = State()
    waiting_for_funcLauncher = State()
    waiting_for_addonsLauncher = State()
    waiting_for_examplesLauncher = State()
    waiting_for_linksLauncher = State()
    waiting_for_designLauncher = State()
    waiting_for_extraInfoLauncher = State()
    waiting_for_deadlineLauncher = State()
    waiting_for_howDouKnowUsLauncher = State()
    waiting_for_sourceLauncher = State()

    #build
    waiting_for_typeBuild = State()
    waiting_for_versionBuild = State()
    waiting_for_whatToBuild = State()
    waiting_for_styleOfBuild = State()
    waiting_for_sizeOfBuild = State()
    waiting_for_detalizationOfBuild = State()
    waiting_for_sezonOfBuild = State()
    waiting_for_pointsOfBuild = State()
    waiting_for_picturesOfBuild = State()
    waiting_for_linksOfBuild = State()
    waiting_for_extraInfoBuild = State()
    waiting_for_deadlineBuild = State()
    waiting_for_sourceBuild = State()

    #site
    waiting_for_nameSite = State()
    waiting_for_siteDomain = State()
    waiting_for_funcSite = State()
    waiting_for_addonsSite = State()
    waiting_for_layoutSite = State()
    waiting_for_examplesSite = State()
    waiting_for_linksSite = State()
    waiting_for_designSite = State()
    waiting_for_extraInfoSite = State()
    waiting_for_deadlineSite = State()
    waiting_for_sourceSite = State()

    #teamcommon
    waiting_for_teamType= State()
    waiting_for_minecraftType= State()
    waiting_for_devType= State()
    waiting_for_fio = State()

    #teamsborshik
    waiting_for_birthdate = State()
    waiting_for_experience = State()
    waiting_for_experienceInServers = State()
    waiting_for_choosePlugin = State()
    waiting_for_problemsInPlugins = State()
    waiting_for_optimizationPluginsOnServer = State()
    waiting_for_tasksOnMigrationsAndUpd = State()
    waiting_for_monitoringProblems = State()
    waiting_for_actualizationOfPlugin = State()
    waiting_for_portfolioPlugin = State()

    #teamplugindev
    waiting_for_fioPlugin = State()
    waiting_for_birthdatePlugin = State()
    waiting_for_experienceInYearsInPlugins = State()
    waiting_for_experiencePlugin = State()
    waiting_for_languagePlugin = State()
    waiting_for_exampleOfPlugin = State()
    waiting_for_optimizationOfPlugin = State()
    waiting_for_databaseOfPlugin = State()
    waiting_for_testsOfPlugin = State()
    waiting_for_compsOfPlugin = State()
    waiting_for_configOfPlugin = State()
    waiting_for_guiOfPlugin = State()
    waiting_for_portfolioPluginNew = State()
