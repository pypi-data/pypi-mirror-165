# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# import matplotlib
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageFilter
import imagehash
from os import walk
import pandas as pd
import os
import wda
import time
import uiautomator2 as u2
import datetime
import subprocess
import argparse
import pyautogui
file_dir = str(__file__).replace(str(__file__).split("/")[-1], "")


class launchtest:

    def __init__(self, package, video_screen=1, run_times=10, ios="http://localhost:8100"):
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

    def mk_folder(self, dir):
        try:
            os.stat(dir)
        except:
            os.makedirs(dir)

    def convert_video_to_screenshot(self, video_file, dir):
        screenshot_path = dir + "/%04d.jpg"
        command = "ffmpeg -i " + video_file + "  -vf fps=5 " + screenshot_path
        process_temp = subprocess.Popen(command, shell=True)
        process_temp.communicate()

    def cut_video(self, device_name, size, different_allow):
        video_path = file_dir + "/recorded_videos/" + device_name + "/video/"
        screen_path = file_dir + "/recorded_videos/" + device_name + "/screenshot/"
        video_list = []
        print("Video Path: " + video_path)
        for (dirpath, dirnames, filenames) in walk(video_path):
            video_list.extend(filenames)
            break
        try:
            video_list.remove(".DS_Store")
        except:
            pass
        for video in video_list:
            self.mk_folder(screen_path + video.replace(".mkv", ""))
            self.mk_folder(screen_path + video.replace(".mkv", "") + "/converted/")
            self.convert_video_to_screenshot(video_path + video, screen_path + video.replace(".mkv", ""))
            self.crop_image(screen_path + video.replace(".mkv", ""), size)
        self.show(device_name=device_name, different_allow=different_allow)

    def crop_image(self, dir, size):
        f = []
        for (dirpath, dirnames, filenames) in walk(dir):
            f.extend(filenames)
            break
        for file in f:
            command = "convert " + dir + "/" + file + " -crop "+size+" " + dir + "/converted/" + file
            process_temp = subprocess.Popen(command, shell=True)
            process_temp.communicate()

    def show(self, device_name, different_allow):
        video_path = file_dir + "/recorded_videos/"+device_name+"/screenshot/"
        for (dirpath_parent, dirnames_parent, filenames_parent) in walk(video_path):
            break
        differences = {}
        data = {}
        start_point = 0
        end_point = 0
        end_point_rule = 10
        for line in dirnames_parent:
            dir = dirpath_parent + line + "/converted/"
            print(dir)
            file = []
            difference = []
            for (dirpath, dirnames, filenames) in walk(dir):
                file.extend(filenames)
            file.sort()
            file_num = 0
            for f in file:
                img1 = Image.open(dir + f)
                img2 = Image.open(dir + file[file_num + 1])
                img1 = img1.filter(ImageFilter.BoxBlur(radius=3))
                img2 = img2.filter(ImageFilter.BoxBlur(radius=3))
                phashvalue = imagehash.phash(img1) - imagehash.phash(img2)
                ahashvalue = imagehash.average_hash(img1) - imagehash.average_hash(img2)
                totalaccuracy = phashvalue + ahashvalue
                if totalaccuracy < different_allow:
                    totalaccuracy = 0
                difference.append(totalaccuracy)
                print(f + " and " + file[file_num + 1] + " : " + str(totalaccuracy))
                file_num += 1
                if file_num == len(file) - 1:
                    break
            differences[line] = difference
        differences = self.mend_list(differences)
        xarray = []
        total_time = 0
        for diff in differences:
            start_point = 0
            end_point = 0
            for i in range(0, len(differences[diff])):
                if differences[diff][i] > 0 and start_point == 0:
                    start_point = 0.2 * i
                    break
            for j in range(0, len(differences[diff])):
                if differences[diff][-(j + end_point_rule)] > 0:
                    end_point = 0.2 * (len(differences[diff]) - 10 - j)
                    break
            launch_time = end_point - start_point
            data[diff.split('.')[-1] + ": " + str(round(launch_time, 2)) + "(s)"] = differences[diff]
            total_time += launch_time

        for diff in differences:
            for i in range(0, len(differences[diff])):
                xarray.append(0.2 * i)
            break
        df = pd.DataFrame(data, index=xarray)
        df.plot()
        plt.title("App Launch time in " + device_name + ": " + str(round(total_time/len(differences), 2)))
        plt.xlabel("App bblt image actions change")
        plt.ylabel("Launch time")
        plt.show()

    def mend_list(self, li):
        len_list = []
        for item in li:
            len_list.append(len(li[item]))
        max_len = max(len_list)
        for item in li:
            for i in range(0, max_len-len(li[item])):
                li[item].append(0)
        return li

    def android_launch_test(self):
        d = u2.connect()
        device_name = d.info['productName']
        print(device_name)
        file_dir = str(__file__).replace(str(__file__).split("/")[-1], "")
        self.mk_folder(dir=file_dir + f"/recorded_videos/{device_name}/video")
        self.mk_folder(dir=file_dir + f"/recorded_videos/{device_name}/screenshot")
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

    def launch_curve(self, device, cut_size="", different_allow=10):
        if "ios" in device:
            device_name = self.ios_launch_test()
        else:
            device_name = self.android_launch_test()
        self.cut_video(device_name, cut_size, different_allow)

    def test_location(self, size):
        pyautogui.screenshot('t.png')
        # point = pyautogui.position()
        # print(point)
        # size = f"{point.x}x{point.y}+780+30"
        convert_str = f"convert 't.png' -crop {size} 'tt.png'"
        process_temp = subprocess.Popen(convert_str, shell=True)
        process_temp.communicate()
        im = Image.open('tt.png')
        im.show()

    def verify_displayed_screens(self):
        global process
        command_linux = "ffmpeg -f avfoundation -list_devices true -i ''"
        process = subprocess.Popen(command_linux, shell=True)
        time.sleep(5)
        if process is not None:
            subprocess.Popen.kill(process)


# if __name__ == '__main__':
    # launchtest("").test_location("1150x1970+10+100")
    # launchtest("").test_location("750x1600+2700+380")
    # launchtest("").show("LYA-AL00", 10)
    # launchtest("com.disney.shanghaidisneyland_goo", run_times=1).launch_curve("android","750x1600+2700+380")
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-os", "--operation_system", default=1, type=int,
    #                     help="Device OS Type, Only Support [1]: IOS & [2]: Android."
    #                          "[0]: Display available screens",
    #                     choices=[0, 1, 2])
    # parser.add_argument("-p", "--package_name", help="APP Package ID")
    #
    # group = parser.add_mutually_exclusive_group()
    #
    # group.add_argument("-vs", "--video_screen", default=1, help="Choose Video Recording Screen")
    # group.add_argument("-size", "--cut_size",
    #                    help="The location of device page cut in recorded video, default: 380x780+710+50")
    #
    # args = parser.parse_args()
    #
    # if args.operation_system == 1:
    #     device_name = launchtest(package=args.package_name).ios_launch_test()
    #     line.make_curve().cut_video(device_name, args.cut_size, 10)
    #     print("ios")
    # elif args.operation_system == 2:
    #     print("android")
    #     device_name = launchtest(package=args.package_name).android_launch_test()
    #     if args.cut_size is not None:
    #         line.make_curve().cut_video(device_name, args.cut_size, 10)
    #     else:
    #         line.make_curve().cut_video(device_name, "600x910+780+30", 10)
    # else:
    #     launchtest().verify_displayed_screens()


# class make_curve:

    # def __init__(self):
    #     pass


#xcodebuild -project ~/Documents/AutoProjects/wda_back/WebDriverAgent/WebDriverAgent.xcodeproj -scheme WebDriverAgentRunner -destination id=00008110-0009549A3EEA801E test