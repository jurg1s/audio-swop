# Audio Swop

A simple tool for swapping audio tracks in video files.

## Installation 

To install Audio Swop, download the .deb package and run the following command:

```bash
sudo dpkg -i audio-swop_<version>_amd64.deb
```

To remove the tool:

```bash
sudo dpkg -r audio-swop
```

## Project Status


> **Status**: 🚧 Early Development  
> **Note**: This project is currently a proof of concept and lacks many essential features. Feel free to contribute, suggest features, or use it for experimental purposes.

```
audio-swop
├─ LICENSE
├─ README.md
├─ releases
│  └─ audio-swop_0.1_amd64.deb
└─ src
   ├─ DEBIAN
   │  ├─ control
   │  └─ postinst
   └─ usr
      ├─ bin
      │  └─ audio_swop
      └─ share
         ├─ applications
         │  └─ audio_swop.desktop
         ├─ audio-swop
         │  ├─ audio_swop.py
         │  ├─ requirements.txt
         │  ├─ setup.sh
         │  └─ spinner.gif
         └─ pixmaps
            └─ icon.png

```