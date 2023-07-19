#!/bin/sh
# Copyright 2019 khanhas. GPL license.
# Edited from project Denoland install script (https://github.com/denoland/deno_install)

set -e

# download uri
releases_uri=https://github.com/spicetify/spicetify-marketplace/releases
if [ $# -gt 0 ]; then
    tag=$1
else
    tag=$(wget -q -O - --header='Accept: application/json' $releases_uri/latest | grep -oE 'tag_name":"v[^"]+' | cut -d'"' -f3)
fi

tag=${tag#v}

echo "FETCHING Version $tag"

download_uri=$releases_uri/download/v$tag/spicetify-marketplace.zip
default_color_uri="https://raw.githubusercontent.com/spicetify/spicetify-marketplace/main/resources/color.ini"

SPICETIFY_CONFIG_DIR="${SPICETIFY_CONFIG:-$HOME/.config/spicetify}"
INSTALL_DIR="$SPICETIFY_CONFIG_DIR/CustomApps"

if [ ! -d "$INSTALL_DIR" ]; then
    echo "MAKING FOLDER  $INSTALL_DIR";
    mkdir -p "$INSTALL_DIR"
fi

TAR_FILE="$INSTALL_DIR/marketplace-dist.zip"

echo "DOWNLOADING $download_uri"
wget -q -O "$TAR_FILE" --no-check-certificate "$download_uri" &> wget_log.txt

if [ $? -ne 0 ]; then
    echo "Failed to download the ZIP file. Check wget_log.txt for details."
    exit 1
fi

cd "$INSTALL_DIR"

echo "EXTRACTING"
unzip -q -d "$INSTALL_DIR/marketplace-tmp" "$TAR_FILE" || {
    echo "Failed to extract the ZIP archive. Check the downloaded file or the ZIP file content in wget_log.txt for details."
    exit 1
}

cd "$INSTALL_DIR/marketplace-tmp"
echo "COPYING"
rm -rf "$INSTALL_DIR/spicetify-marketplace/" "$INSTALL_DIR/marketplace/"
mv "$INSTALL_DIR/marketplace-tmp/spicetify-marketplace-dist" "$INSTALL_DIR/marketplace"

echo "INSTALLING"
cd "$INSTALL_DIR/marketplace"

# Remove old custom app name if exists
spicetify config custom_apps spicetify-marketplace-

# Color injection fix
spicetify config inject_css 1
spicetify config replace_colors 1

current_theme=$(spicetify config current_theme)
if [ ${#current_theme} -le 3 ]; then
    echo "No theme selected, using placeholder theme"
    if [ ! -d "$SPICETIFY_CONFIG_DIR/Themes/marketplace" ]; then
        echo "MAKING FOLDER  $SPICETIFY_CONFIG_DIR/Themes/marketplace";
        mkdir -p "$SPICETIFY_CONFIG_DIR/Themes/marketplace"
    fi
    wget -q -O "$SPICETIFY_CONFIG_DIR/Themes/marketplace/color.ini" --no-check-certificate "$default_color_uri"
    spicetify config current_theme marketplace;
fi

if spicetify config custom_apps marketplace ; then
    echo "Added to config!"
    echo "APPLYING"
    spicetify apply
else
    echo "Command failed"
    echo "Please run \`spicetify config custom_apps marketplace\` manually "
    echo "Next run \`spicetify apply\`"
fi

echo "CLEANING UP"
rm -rf "$TAR_FILE" "$INSTALL_DIR/marketplace-tmp/"
