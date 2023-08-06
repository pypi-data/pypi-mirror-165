# Paper-Secret

Shamir Secret Sharing on paper using gfshare.

## Installation

### PyPi

* https://pypi.org/project/paper-secret/

### Dependencies

`gfshare` is required to split and merge the secret.
See `man gfshare` for an explanation of Shamir Secret Sharing in gf(2**8).

```shell
sudo pacman -S --needed libgfshare
```

`qrencode` and `imagemagick` (`convert`) are required to create and merge QR-codes during the split process.
One can set the according parameters of `split_encode` to `False` to skip this step.

```shell
sudo pacman -S --needed qrencode imagemagick
```

`enscript` and `ghostscript` (`ps2pdf`) are required to create a PDF containing the split secret in text form.
One can set the according parameters of `split_encode` to `False` to skip this step.

```shell
sudo pacman -S --needed enscript ghostscript
```

## Usage

Create a secret:

```shell
cat > secret.txt
```

Split the secret into 5 lines:

```shell
enpaper secret.txt
```

Manually delete up to 2 of the 5 lines in `secret.txt_txt.txt`.

Then recreate the secret:

```shell
depaper secret.txt.split-text.txt
```

Print the secret:

```shell
cat secret.txt.split-text.txt.merged.txt
```

## Notes

* https://en.wikipedia.org/Shamir's_Secret_Sharing
