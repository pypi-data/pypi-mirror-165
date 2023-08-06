# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)[^1].

<!---
Types of changes

- Added for new features.
- Changed for changes in existing functionality.
- Deprecated for soon-to-be removed features.
- Removed for now removed features.
- Fixed for any bug fixes.
- Security in case of vulnerabilities.

-->

## [Unreleased]

## [2.2.12] - 2022-08-30

### Changed

* UploadSGPlayblasts: Checks if the revision file exists, if not, the shot status is set to warning and cannot be selected.

### Fixed

* CompareWithAnimatic: If there is no compositing preview in the shot, the user can choose to open the animatic.
* CompareInRV: Revisions of animatic is hidden if the file is the animatic.
* CompareCompMovies: Revisions of animatic is hidden if there are not at least two revisions of compositing preview.
* Background retiming when updating a compositing scene.
* Layout package creation when only the PSD file is packed, while no revision of the package has yet been created on the current site.

## [2.2.11] - 2022-08-08

* Packaging: `CreateLayoutPackagesAction` has an option to take only `.psd` files for package creation.

## [2.2.10] - 2022-08-04

### Changed

* CreateSGShots: Can no longer be used from the list of sequences with a right click.

### Added

* Packaging: `CreateCleanPackagesAction` now sends a delivery email when packages are uploaded.

## [2.2.9.1] - 2022-08-04

### Fixed

* `CreateCleanPackagesAction` which was no longer working after the display of the package size in the `CreateLayoutPackagesAction` was introduced.

## [2.2.9] - 2022-08-03

### Added

* Packaging: `CreateLayoutPackagesAction` now sends a delivery email when packages are uploaded.

## [2.2.8] - 2022-08-02

### Added

* Packaging: The size of each package is now displayed in the list.

### Changed

* Initiate shot: 
  - Ignore `Todo` status in Kitsu tasks.
  - Set the project working space to `sRGB`.

### Fixed

* The prefix `anim_` has been added to the name of the compositions containing animation layers in a compositing scene at initialisation. It ensures that the names of these compositions is different from the main composition name, which is the one used to render playblasts.
* Animation layers and background of a compositing scene are no longer updated if their versions have already been imported.

## [2.2.7] - 2022-07-21

## Changed

### Authentication

* A user now logs in with a login defined in its profile. The password is that of the Kitsu account being used by the user.

## [2.2.6] - 2022-06-28

### Added

#### Initialisation and update of compositing scenes

* `compositing` tasks hold two actions to initialise and update a compositing scene `compositing.aep`.
  - **Initialisation**: imports the latest revisions of the following elements, if available:
    - animatic (`misc/animatic.mp4`)
    - soundtrack (`misc/audio.wav` or `misc/audio`)
    - background (`misc/background.psd`)
    - clean-up layers (`clean/layers`)
    
    More specifically:
    - the background scene and clean-up layers are imported under a folder with the name of their revision (e.g., `v003/background.psd`).
    - the audio track of the video reference and animatic are disabled.
    - are imported as guide layers in the main composition, each layer of the background whose name contains one of the following labels: *CAMERA*, *LABEL*, *BRIEFING* and *DIALOGUE*.
  - **Update**: updates the existing background and layers to their latest revisions.

When initialising/updating a scene, the duration of the footages and compositions in the imported background project (including the parent composition) is automatically set to the duration of the main composition.

#### Unpacking

* The user can set a target according to the action presets. An option to ignore the file has also been added.
* Additional target statutes to be updated for a shot on Kitsu and Shotgrid can be defined in the unpacking presets. The updated statutes for a shot are the union of the statutes of all matched presets.
* A match count limit for each unpacking target. If the number of matches exceeds this limit, only the target of the first match among the conflicting matches is defined. The targets of the remaining matches are then to be specified by the user.
* The user can specify custom relative path and name for unpacked files in the action presets, which can containing special keys:
  - `{film}`, `{sequence}` and `{shot}`
  - `{parent_folder}`: the name of the parent folder of the file in the source package

#### Creation of default files

* Each task holds an option to create default files according to the default task configuration in the project's task manager.

### Changed

* Unpacking: the base name of a file sequence (i.e., the name preceeding the range in the format) is automatically renamed with the name of the parent folder in the relative path.
* CompareInRV: Only the sound of the first revision is enabled.
* UploadSGPlayblasts: 
    - Default size of the action enlarged
    - Simplified file name for the version code of the shot in ShotGrid.
      `compositing_movie` > `comp`

### Fixed

#### Unpacking

* When the list of shots is updated, the total number is now also refreshed.
* When multiple presets have the same target, make sure these presets use their own match count limit.
* When typing the target manually, the display is no longer cut off.

## [2.2.5] - 2022-06-23

### Added

* Embed the code of the ShotGun API (version 3.3.2).

## [2.2.4] - 2022-06-20

### Added

* The user can now specify the value to use for a package creation parameter through an environment variable, or setting a value to use for each OS (among Windows, Linux and Darwin). The environment variable (whose name is specified in the `environ_var_name` parameter) is retrieved first. If undefined, the value specified for the OS currently running is used.

## [2.2.3] - 2022-06-16

### Changed

* Packaging: `CreateLayoutPackagesAction` is no longer based on `clean` task to create packages.
* Define an action for each file of a shot to open, available in a submenu right-clicking on the shot in the map.

### Added

* Unpacking: The number of shots is now shown in the interface.

### Fixed

* Unpacking: Replace a deprecated Qt function that was causing the action not to work.
* `OpenLastFilesAction`: Redefine the right attribute to check if the `sources` folder exists and display the warning message if it doesn't.

## [2.2.2] - 2022-06-09

### Added

* ShotGrid API wrapper: Define a method to create and upload a version in a shot

* An action in the films to upload compositing playblasts to ShotGrid:
  - It lists all shots with status `WFA` on Kitsu
  - When a shot is uploaded, its status on Kitsu is changed to `WFA_SG`
  - Every shot upload is reported in a log file located in `PRODUCTION\delivery` folder.

## [2.2.1] - 2022-06-08

### Added

* A file in `.mp4` or `.mov` now has options to:
  - Compare revisions in RV with column layout. Revisions of shot animatic (`misc/animatic.mp4` by default) can be chosen and added.
  - Compare with shot animatic (`misc/animatic.mp4` by default) in RV.
* `layers` folders in `clean` tasks have an option to open the animation layers they contain in RV.
* A shot now has options to:
  - Open the last background file in Photoshop
  - Open the last compositing file in After Effects
  - Open the sources folder
  - Compare revisions of compositing preview (`compositing/compositing_movie.mov` by default) in RV. Revisions of animatic (`misc/animatic.mp4` by default) can be chosen and added.
  - Open last files revisions:
    - Background file in Photoshop
    - Compositing file in After Effects
    - Sources folder

### Changed

* `OpenAnimationLayers` in a shot is now merged in `OpenLastFiles`.

### Fixed

* `CompareWithAnimaticAction` in a shot now get the last revision file only if its available on current site.

## [2.2.0] - 2022-06-08

### Added

* Redefine the types of tracked files and folders in the project, inheriting from the types available in libreflow.

## [2.1.1] - 2022-05-18

### Added

* Add default shotgrid login group to project settings.
* Every working site can now have a custom shotgrid login.
* A file map has now an action to compare two revisions from a `.mp4` or `.mov` file in Shotgun RV with column layout.

## [2.1.0] - 2022-05-18

### Added

* The ShotGridEntity class which defines an entity on ShotGrid, whose id is stored in the `shotgrid_id` parameter.
* Whenever a shot is created, its tasks are created according to the default tasks defined in the project's task manager.

### Changed

* The option to create a film's sequences based on ShotGrid data has been made available on the film. Similarly, the option to create a sequence's shots based on ShotGrid data has been moved into the sequence.
* Types related to films, sequences and shots now inherit from that defined in Libreflow. These entities are stored in the global collections hold by the entity manager.
* For semantic purposes, shot departments have been redefined as **tasks**. Plus, tasks are defined in a map to allow more flexibility when dealing with particular cases in the production of shots.

## [2.0.12] - 2022-05-13

### Added

* Unpacking:
  - Revisions are automatically uploaded to the exchange server.
  - The shot list is refreshed after the unpacking has finished.
  - Layout: The ShotGrid compositing briefing of a shot is added as a comment to its Kitsu *Compositing* task, if the status of the latter is *TODO*. The comment defaults to `No comment` if the briefing is undefined.
* A shot's compositing briefing can be retrieved with the Shotgun wrapper's `get_shot_comp_briefing()` method.
* A shot now has options to:
  - compare its compositing preview (`compositing/compositing_movie.mov` by default) with its animatic (`misc/animatic.mp4` by default) in RV.
  - open its animation layers in RV
* Use Sentry to monitor events of the GUI session. The Sentry SDK is initialised before starting the session, assuming the project Data Source Name (DSN) is provided in the `SENTRY_DSN` environment variable.

### Fixed

* Unpacking: the package list is not updated anymore whenever the dialog shows up (only the first time, or when the list is explicitly refreshed).
* Expand synchronisation field in the project's root by default.

## [2.0.11] - 2022-04-26

### Added

* An action to export files of shots filtered by their Kitsu statutes.

## [2.0.10] - 2022-04-25

### Added

* Unpacking: add an option to automatically delete packages on the current site if they were uploaded.

### Fixed

* Unpacking action display when files are ignored.
* Ensure Kitsu host is defined when the project is entered through the home page `sequences` button.

## [2.0.9] - 2022-04-21

### Added

* An action in the films allowing to unpack the content of packages into specific files and folders. The content may be single files or file sequences, and currently follow these rules:
  - a single file is unpacked as a new revision of a tracked file
  - a single file/file sequence is unpacked into a new revision of a tracked folder, with its subdirectories in the source package
  - multiple elements assigned to a same target folder will be unpacked into the same revision
* An AfterEffects scene template
* A JSX script defining a set of functions to import elements for initialising a compositing scene
* A method to the Shotgun API wrapper to get a shot's duration.
* An action to initialise a compositing scene with the following elements (latest revision in each case), if they do exist:
  - background: `misc/background.mp4`
  - animatic: `misc/animatic.mp4`
  - video reference: `misc/video_ref.mp4`
  - audio tracks: all WAV files found in the folder `misc/audio`
  - clean-up layers: all PNG sequences found in the folder `clean/layers`

## [2.0.8] - 2022-04-04

### Added

* Packaging:
  - `CreateCleanPackagesAction` holds a list of presets of the source files that have to be packed.
  - An action to select the type of packages (clean or layout) to create, which prompts the dialog of the appropriate action.

### Changed

* Packaging: `CreateCleanPackagesAction` creates a single type of package.

### Fixed

* Layout package creation when multiple sources are packed

## [2.0.7] - 2022-04-01

### Added

* An action to create clean-up packages

### Changed

* Allow to pack multiple source folders into a single package

## [2.0.6] - 2022-04-01

### Changed

* Create packages:
  - allow packages of a shot to be created in case the color is available on SG but source files don't exist on disk. In that case, color files are considered as to be sent from another site.
  - create color package only if it's available on SG

### Fixed

* When a package is created, the name of its latest revision is updated in the file list.

## [2.0.5] - 2022-03-30

### Added

* Add action value store

## [2.0.4] - 2022-03-21

### Changed

* Packages: Create a new target folder whenever the creation of packages is launched.

## [2.0.3] - 2022-03-21

### Added

* A ShotGrid API wrapper providing operators to get and update shot tasks.

### Changed

* The `CreateShotPackages` action lists all shots with a specific task on ShotGrid server having a specific status.

## [2.0.2] - 2022-03-13

### Added

* Prettier labels for sequences, shots and departments
* Search flow views, which allow to browse project indexed entries. This feature relies on the search module included in Libreflow, which makes use of a MongoDB for entry indexation. Thus, the feature can be enabled giving the session the URI configuration string of this database. If not provided, flow views revert to their default behaviour.

## [2.0.1] - 2022-03-13

### Added

* An option to pack directories into existing shots.
* An option to create packages, based on predefined templates.
* Register runners required to:
  - edit AfterEffects scenes (`AfterEffects`)
  - render image sequences (`AfterEffectsRender`)
  - mark rendered images (`MarkSequenceRunner`)

### Fixed

* Error raising when the home page *Sequences* button was clicked

## [2.0.0] - 2022-02-08

Define a flow up and ready to use.