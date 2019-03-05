"""
If this is borken for you it's because it's absolute paths. I'll work on that :)

This file contains code to create icons
you need two files

1. icon_todo.txt with a list of mtl and xml names to create icons for
    object/path/to1.mtl,XmlItemName1
    object/path/to2.mtl,XmlItemName2
    object/path/to3.mtl,XmlItemName3
    object/path/to4.mtl,XmlItemName4


2. icon_done.txt
    log file of all created icons used to rename the last created icon
    CLEAR THIS OUT BEFORE YOU START!

3. CLEAR OUT YOUR SCREENSHOTS FOLDER SO IT'S EMPTY!
    CLEAR OUT D:\perforce\dev\user\screenshots

4. Open icon_level.cry

5. run icon_object_add.py and set the name of the Item you are creating or Group Category in the spawner
    If you are retaking an icons grab the position of the items using icon_object_get.py and it will update the object
    to the stored pose of the icon

6. Open python Scripts Panel

7. Click create_batch_icons.py until it tells you to stop clicking

8. Run the photoshop action - This automatically creates the icons in the correct spot

9. Add and commit icons added from photoshop action.
"""
import os
import time
import general


class IconBatcher(object):
    """Creates Icons"""

    def __init__(self):
        super(IconBatcher, self).__init__()
        self.icon_file_todo = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "iconfile_todo.txt"))
        self.icon_file_done = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "iconfile_done.txt"))
        self.screenshot_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__),'..','..','user','screenshots'))
        self.scrnsht_0 = os.path.abspath(
            os.path.join(self.screenshot_dir, "screenshot0000.jpg"))
        self.output_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__),'..','..','user','screenshots'))
        self.xml = str()
        self.mtl = str()
        self.last_xml = str()
        self.last_mtl = str()
        self.first_shot = False
        self.get_set_xml_mtl()
        self.first_setup()
        self.last_image = False
        self.icon_img = str()

    def first_setup(self):
        # if the screenshot doesn't exist do some initial setup
        if not os.path.exists(self.scrnsht_0):
            self.first_shot = True
            # create the first screenshot
            self.take_shot()
            # set the first material
            self.set_mat()
            # set the done file without removing the top linein todo
            # self.write_mat()
        else:
            self.get_set_last_xml_mtl()

    def clear_done_file(self):
        print('clearing done file')
        data = []
        with open(self.icon_file_done, 'w') as fout:
            fout.writelines(data)

    def get_set_last_xml_mtl(self):
        '''reads a icon_done and gets and sets the top mtl and xml from it'''
        with open(self.icon_file_done, 'r') as f:
            try:
                mtl, xml = f.readline().rstrip().split(',')
                self.last_xml = xml
                self.last_mtl = mtl
            except Exception as e:
                self.last_xml = self.xml
                self.last_mtl = self.mtl

    def get_set_xml_mtl(self):
        '''reads a file and gets and sets the top mtl and xml from it'''

        try:
            with open(self.icon_file_todo, 'r') as f:
                mtl, xml = f.readline().rstrip().split(',')
                self.xml = xml
                self.mtl = mtl
        except Exception as e:
            self.last_image = True
            general.message_box_ok('No More Icons Stop Clicking')
            self.rename_last_image()

    def rename_last_image(self):
        self.get_set_last_xml_mtl()
        os.rename(self.scrnsht_0, '%s\%s_48.jpg' % (self.screenshot_dir, self.last_xml))
        self.last_image = True

    def write_mat(self):
        '''writes the self.mtl and self.xml to self.icon_file_done as self.mtl,self.xml'''
        with open(self.icon_file_done, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            line = '%s,%s' % (self.mtl, self.xml)
            f.write(line.rstrip('\r\n') + '\n' + content)

    def take_shot(self):
        # take screenshot
        time.sleep(0.05)
        general.run_console('r_getScreenshot 1')

    def set_mat(self):
        general.set_custom_material('icon_object_shot', str(self.mtl))

    def rename_image(self):
        # renames self.scrnsht_0 to self.xml
        try:
            self.icon_img = '%s\%s_48.jpg' % (self.screenshot_dir, self.last_xml)
            os.rename(self.scrnsht_0, self.icon_img)
            self.process_image()
        except Exception as e:
            print (e)
            os.remove(self.scrnsht_0)

    def process_image(self):
        print ('processing %s' % self.icon_img)

    def remove_top_line(self):
        with open(self.icon_file_todo, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(self.icon_file_todo, 'w') as fout:
            fout.writelines(data[1:])

    def button_pressed(self):
        '''this is called each time the button is pressed in the editor'''
        if self.first_shot:
            print ('Initial Set up')
        else:
            print (' renaming image for %s' % self.last_xml)
            self.rename_image()
            print ('applying %s to icon_object_shot' % self.mtl)
            self.set_mat()
            print ('creating image for %s' % self.xml)
            self.take_shot()
            print ('removing top line in todo')
            self.remove_top_line()
            self.write_mat()


def main():
    ib = IconBatcher()
    ib.button_pressed()


if __name__ == '__main__':
    main()
