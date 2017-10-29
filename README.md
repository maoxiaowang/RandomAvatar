# RandomAvatar
To generate random pixel avatars with Pillow

## Example
1 Initialization

    a = Avatar()

2 Generate a avatar with 256(default) px width and height

    avatar = a.generate_avatar(fp=r'D:\test', fn='avatar.jpg')
    
3 Generate two thumbnails from the generated avatar, 40x40 and 100x100 respectively

    a.generate_thumb(avatar, size=100, fn='avatar_thumb_100x100.jpg')
    a.generate_thumb(avatar, size=40, fn='avatar_thumb_40x40.jpg')

![image](https://github.com/maoxiaowang/RandomAvatar/raw/master/screenshots/2.jpg)