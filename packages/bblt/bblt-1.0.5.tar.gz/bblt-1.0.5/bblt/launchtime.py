# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import matplotlib

from build.lib.bblt import line

matplotlib.use('Agg')
import os
import wda
import time
import uiautomator2 as u2
import datetime
import subprocess
import argparse


main_activity = ''
screen = 3


class launchtest:

    def __init__(self, package, video_screen=3, run_times=10, ios="http://localhost:8100"):
        self.screen = video_screen
        self.times = run_times
        self.ios_host = ios
        self.package_name = package

    def start_video(self, video_path):
        global process
        command_linux = f"ffmpeg -f avfoundation  -video_device_index {self.screen} -i ':' {video_path}"
        process = subprocess.Popen(command_linux, shell=True)

    def pause_video_recording(self):
        time.sleep(10)
        if process is not None:
            subprocess.Popen.kill(process)

    @classmethod
    def android_launch_test(self):
        d = u2.connect()
        device_name = d.info['productName']
        file_dir = str(__file__).replace(str(__file__).split("/")[-1], "")
        self.mk_folder(file_dir + f"/recorded_videos/{device_name}/video")
        self.mk_folder(file_dir + f"/recorded_videos/{device_name}/screenshot")
        print(f'\n\n=======Android Device {device_name} Launch Time Test Started ========\n')
        for x in range(0, self.times):
            start_time = str(datetime.datetime.now()).replace(" ", "_")
            video_path = file_dir + f"/recorded_videos/{device_name}/video/video_{start_time}.mkv"
            d.app_stop_all()
            time.sleep(5)
            self.start_video(video_path)
            time.sleep(5)
            d.session(self.package_name)
            time.sleep(15)
            # d(resourceId="com.disney.shanghaidisneyland_goo:id/img_avatar").wait()
            self.pause_video_recording()
            d.app_stop(self.package_name)
        print('\n\n=======Android Launch Time Test Stopped ========\n')
        return device_name

    @classmethod
    def launch_curve(self, device, cut_size="", different_allow=10):
        if "ios" in device:
            if cut_size == "":
                cut_size = "600x910+780+30"
            device_name = self.ios_launch_test()
        else:
            if cut_size == "":
                cut_size = "380x780+710+50"
            device_name = self.android_launch_test()
        line.make_curve().cut_video(device_name, cut_size, different_allow)

    @classmethod
    def ios_launch_test(self):
        c = wda.Client(self.ios_host)
        device_name = c.info['name'].replace(" ", "")
        file_dir = str(__file__).replace(str(__file__).split("/")[-1], "")
        self.mk_folder(file_dir + f"/recorded_videos/{device_name}/video")
        self.mk_folder(file_dir + f"/recorded_videos/{device_name}/screenshot")
        element = c(label=u"餐饮")
        # element = c(label=u"Park Info & Entry")
        print(c.info)
        print(f'\n\n======= IOS Device {device_name} Launch Time Test Started =======\n')
        for x in range(0, self.times):
            # start_time = str(datetime.datetime.now()).replace(" ", "_")
            file_dir = str(__file__).replace(str(__file__).split("/")[-1], "")
            video_path = file_dir + f"/recorded_videos/{device_name}/video/video_{device_name}.mkv"
            time.sleep(5)
            self.start_video(video_path)
            time.sleep(5)
            c.session(self.package_name)
            # element.wait()
            # if element.exists or elementA.exists:
            #     element.click()
            time.sleep(5)
            self.pause_video_recording()
            c.close()
        print('\n\n======= IOS Launch Time Test Stopped ========\n')
        return device_name

    def mk_folder(self, dir):
        try:
            os.stat(dir)
        except:
            os.makedirs(dir)

    def verify_displayed_screens(self):
        global process
        command_linux = "ffmpeg -f avfoundation -list_devices true -i ''"
        process = subprocess.Popen(command_linux, shell=True)
        time.sleep(5)
        if process is not None:
            subprocess.Popen.kill(process)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-os", "--operation_system", default=1, type=int,
                        help="Device OS Type, Only Support [1]: IOS & [2]: Android."
                             "[0]: Display available screens",
                        choices=[0, 1, 2])
    parser.add_argument("-p", "--package_name", help="APP Package ID")

    group = parser.add_mutually_exclusive_group()

    group.add_argument("-vs", "--video_screen", default=1, help="Choose Video Recording Screen")
    group.add_argument("-size", "--cut_size",
                       help="The location of device page cut in recorded video, default: 380x780+710+50")

    args = parser.parse_args()

    if args.operation_system == 1:
        device_name = launchtest(package=args.package_name).ios_launch_test()
        line.make_curve().cut_video(device_name, args.cut_size, 10)
        print("ios")
    elif args.operation_system == 2:
        print("android")
        device_name = launchtest(package=args.package_name).android_launch_test()
        if args.cut_size is not None:
            line.make_curve().cut_video(device_name, args.cut_size, 10)
        else:
            line.make_curve().cut_video(device_name, "600x910+780+30", 10)
    else:
        launchtest().verify_displayed_screens()

#xcodebuild -project ~/Documents/AutoProjects/wda_back/WebDriverAgent/WebDriverAgent.xcodeproj -scheme WebDriverAgentRunner -destination id=00008110-0009549A3EEA801E test