# Maintainer: Arthur Williams <taaparthur@gmail.com>


pkgname='indent-sort'
pkgver='0.1.0'
_language='en-US'
pkgrel=1
pkgdesc='Sort text with respect to indentation'

arch=('any')
license=('MIT')
depends=('python')
md5sums=('SKIP')

source=("git+https://github.com/TAAPArthur/indent-sort.git")
_srcDir="indent-sort"

package() {
  cd "$_srcDir"
  install -D -m 0755 "indent-sort.py" "$pkgdir/usr/bin/$pkgname"
}
