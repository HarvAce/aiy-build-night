# aiy-build-night

This repo is the one-stop-shop for anything do-it-yourself artificial intelligence (AIY) build night.

We will be continuing to update this repository leading up to the event!

## Hardware

There are two different kits that can be used: a voice kit and a camera kit. If you would like to bring your build home with you, you need to prepurchase the kit from any vendor. Also, if you would like to work with the camera kit, you should plan to prepurchase, as there will only be a few available.

The suggested purchase list is:
- [SanDisk MicroSDHC 16GB ($6.95)](https://www.amazon.com/SanDisk-Mobile-MicroSDHC-SDSDQM-B35A-Adapter/dp/B004ZIENBA)
- [AIY Voice Kit ($9.99)](https://www.amazon.com/Google-GOOGLEAIY-V1-AIY-Voice/dp/B075SFLWKX)
- [Raspberry Pi 3 Kit w/Power Supply ($42.00)](https://www.amazon.com/CanaKit-Raspberry-Micro-Supply-Listed/dp/B01C6FFNY4)

OR

- [AIY Vision Kit ($89.99)](https://www.target.com/p/google-vision-kit-aiy/-/A-53417081)

## Software

You will need to install software on your personal laptop in order to communicate with your kit.
The following steps need to be completed to be able to communicate and work with each kit:

- Install the VNC Viewer application in order for your laptop to communicate with the Raspberry PI boards
  - https://www.realvnc.com/en/connect/download/viewer
- Install the Google AIY Raspbian software on the SD Card you will use with your kit (if you purchased a kit)
  - Download Google's [Voice Kit SD image](https://dl.google.com/dl/aiyprojects/aiyprojects-latest.img.xz)
  - Download [Etcher.io](https://etcher.io/) to burn Voice Kit image onto SD card 
  - Launch Etcher and follow instructions

## Setting up Google Cloud Credentials

If you are bringing your own kit you can optionally set up a Google Cloud account ahead of the build night.  Follow the intructions below to create and download the credentials to your computer.

- https://aiyprojects.withgoogle.com/voice/#google-assistant--get-credentials

## Connect to Your Kit

1. Connect your laptops to the Build Night wifi. The provided boards will automatically connect to the Build Night wifi (you will need to manually configure your board to connect to the Build Night wifi if you brought your board with you).
2. Open VNC Viewer on your laptop.
3. Connect to your-board-name.local, such as chips.local (written on your kit box).

## AIY Instructions
- Voice Kit: https://aiyprojects.withgoogle.com/voice-v1/
- Vision Kit: https://aiyprojects.withgoogle.com/vision/
