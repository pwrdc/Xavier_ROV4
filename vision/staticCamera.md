<h2> Jak ustawić statyczne odniesienie do kamery, aby móc zawsze łączyć się z tą samą kamerą z poziomu opencv? </h2>

Należy

<li>Przełączyć się na użytkownika 'root' stosując komendę: <br/><br/> </li>

```console
nvidia@nvidia-desktop:~$ sudo su
```




<li>Następnie dla każdej kamery dla której ustawiany jest alias należy zastosować komendę:<br/><br/>

```console
root@nvidia-desktop:~$ udevadm info -a -p $(udevadm info -q path -p /class/video4linux/video*)
```
&nbsp;&nbsp;&nbsp;&nbsp; zastępując '*' cyfrą urządzenia. Opis kamer można podejrzeć komendą:

```console
nvidia@nvidia-desktop:~$ v4l2-ctl --list-devices
```

&nbsp;&nbsp;&nbsp;&nbsp; z zainstalwoanym pakietem v4120ctl:

```console
nvidia@nvidia-desktop:~$ sudo apt-get install v4l-utils
```

<li>
Wyjście poprzedniej komenty zawiera linijkę, wyglądającą tak: 
</li>

```console
ATTRS{serial}=="520EE700"
```
<li>
W katalogu /etc/udev/rules.d/ należy utworzyć plik zawierający regułę wiążącą urządzenia z aliasem
(obecnie w xavierze &nbsp;&nbsp;&nbsp;&nbsp;istnieje już taki plik "15-auv-cameras.rules"). W pliku tym należy dodać nastepującą linijkę:</li>

```console
SUBSYSTEM=="video4linux", ATTRS{serial}=="********", SYMLINK+="*********"
```
&nbsp;&nbsp;&nbsp;&nbsp;Uzupełniając ATTRS{serial} numerem seryjnym urządzenia oraz SYMLINK aliasem, który będzie używany do 
łączenia się &nbsp;&nbsp;&nbsp;&nbsp;z kamerą<br/><br/>


<li>
Zresetować urządzenie, kamery powinny być dostępne. Przykład korzystania z poziomu Pythona:</li>

```python
camera = cv2.VideoCapture("/dev/utworzony_alias")
```

&nbsp;&nbsp;&nbsp;&nbsp;Obecnie istnieją 2 aliasy: camera_c922_1, camera_hdpc_1.




