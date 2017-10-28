# RandomAvatar
To generate random pixel avatar with Pillow

## Example
1 Initialization

    a = Avatar()

2 Generate a 256 px width and height avatar

    avatar_path = a.generate_avatar(256, '')
    
3 Generate two thumbs from the generated avatar, 40x40 and 100x100

    a.generate_avatar_thumbs(_, sizes=(40, 100))

![image](https://github.com/maoxiaowang/RandomAvatar/raw/master/screenshots/1.jpg)