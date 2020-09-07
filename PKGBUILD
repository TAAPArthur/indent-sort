# Maintainer: Arthur Williams <taaparthur@gmail.com>


pkgname='indent-sort'
pkgver='1.1'
_language='en-US'
pkgrel=0
pkgdesc='Sort text with respect to indentation'

arch=('any')
license=('MIT')
depends=(python)
md5sums=('SKIP')

source=("git+https://github.com/TAAPArthur/indent-sort.git")
_srcDir="indent-sort"

package() {
  cd "$_srcDir"
  DESTDIR=$pkgdir make install
}
