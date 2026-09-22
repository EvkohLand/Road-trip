#!/usr/bin/env bash
# Derived images for SEO / social previews. Run after changing a source photo.
# Needs ImageMagick (convert). Outputs are committed: CI does not regenerate them.
set -euo pipefail
cd "$(dirname "$0")/../dist/assets"
# Open Graph / Twitter previews: 1200x630 is the size every network crops to.
convert road.jpg -resize 1200x630^ -gravity center -extent 1200x630 -quality 82 -strip og-default.jpg
convert setup-tv.jpg -resize 1200x630^ -gravity north -extent 1200x630 -quality 82 -strip og-cinema-tente-de-toit.jpg
# Lighter setup photo for phones (srcset 800w).
convert setup-tv.jpg -resize 800x -quality 78 -strip setup-tv-800.jpg
# Hero photo: phone-sized variant + WebP versions (Lighthouse "modern image formats").
convert road.jpg -resize 800x -quality 78 -strip road-800.jpg
for f in road road-800 setup-tv setup-tv-800; do convert "$f.jpg" -quality 78 "$f.webp"; done
# App / bookmark icons from the favicon design (dark green tile, white road).
# Drawn with primitives: ImageMagick's internal SVG renderer drops the white strokes.
icon() { # size, output, background(none|color)
  local n=$1 k; k=$(echo "$1/40" | bc -l)
  local rx; rx=$( [ "$3" = none ] && echo "10" || echo "0" )
  convert -size "${n}x${n}" xc:"$( [ "$3" = none ] && echo none || echo "$3")" \
    -fill '#173f35' -draw "scale $k,$k roundrectangle 0,0 40,40 $rx,$rx" \
    -stroke white -fill none -strokewidth 2 \
    -draw "scale $k,$k polyline 12,34 17,6 23,6 28,34" \
    -draw "scale $k,$k line 20,9 20,14 line 20,19 20,24 line 20,29 20,34" "$2"
}
icon 512 icon-512.png none
icon 180 apple-touch-icon.png '#173f35'
icon 32 favicon-32.png none
