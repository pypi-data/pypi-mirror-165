#!/usr/bin/env python3
import sys
import os
from os.path import join
import subprocess
from pathlib import Path
import time
import subprocess
import shlex
from .. import settings
from os import path
import threading
import yaml
import logging
from mtlibs import process_helper
from mtlibs import mtutils
import platform
import shutil
import subprocess

logger = logging.getLogger(__name__)


class WordPressService():
    def __init__(self):
        self.html_root = settings.getHtmlRoot()
        self.logdirBase = settings.getLogDirBase()
        self.logfile = open(os.path.join(self.logdirBase,".wordPress_depploy.log"), "a")
        self.error = None
    def start(self):
        logger.info("启动 WordPressService ")        
        self.deploy_wordpress(self.html_root)

    def stop(self):
        logger.info("TODO: stop wordpress")
        pass

    def write_log(self, message: str):
        self.logfile.write(f"{message}\n")
        self.logfile.flush()


    def deploy_wordpress(self, deployToDir:str):    
        logger.info("clone wordpress.....")
        gitclone_dir = "/tmp/wordpress"
        process_helper.exec(f"""rm -rdf {gitclone_dir}""")
        cp_clonewordPress = subprocess.run(
            shlex.split(
            f"""git clone --depth=1 https://github.com/WordPress/WordPress.git {gitclone_dir}""",
            ),
            stderr=self.logfile, 
            stdout=self.logfile
        )
        if cp_clonewordPress.returncode != 0:
            # print("clone wordpress Fail!")
            self.error = "clone wordpress Fail!"
            self.write_log(self.error)
            return

        shutil.copytree(gitclone_dir, deployToDir, dirs_exist_ok=True)
        process_helper.exec(f"""rm -rdf /tmp/wordpress""")

        self.write_log("设置wordpress wp-config.php")
        wp_config = """<?php
/**
* The base configuration for WordPress
*
* The wp-config.php creation script uses this file during the installation.
* You don't have to use the web site, you can copy this file to "wp-config.php"
* and fill in the values.
*
* This file contains the following configurations:
*
* * Database settings
* * Secret keys
* * Database table prefix
* * ABSPATH
*
* This has been slightly modified (to read environment variables) for use in Docker.
*
* @link https://wordpress.org/support/article/editing-wp-config-php/
*
* @package WordPress
*/

// IMPORTANT: this file needs to stay in-sync with https://github.com/WordPress/WordPress/blob/master/wp-config-sample.php
// (it gets parsed by the upstream wizard in https://github.com/WordPress/WordPress/blob/f27cb65e1ef25d11b535695a660e7282b98eb742/wp-admin/setup-config.php#L356-L392)

// a helper function to lookup "env_FILE", "env", then fallback
if (!function_exists('getenv_docker')) {
    // https://github.com/docker-library/wordpress/issues/588 (WP-CLI will load this file 2x)
    function getenv_docker($env, $default) {
        if ($fileEnv = getenv($env . '_FILE')) {
            return rtrim(file_get_contents($fileEnv), "\r\n");
        }
        else if (($val = getenv($env)) !== false) {
            return $val;
        }
        else {
            return $default;
        }
    }
}

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', getenv_docker('WORDPRESS_DB_NAME', 'wordpress') );
/** Database username */
define( 'DB_USER', getenv_docker('WORDPRESS_DB_USER', 'example username') );

/** Database password */
define( 'DB_PASSWORD', getenv_docker('WORDPRESS_DB_PASSWORD', 'example password') );

/**
* Docker image fallback values above are sourced from the official WordPress installation wizard:
* https://github.com/WordPress/WordPress/blob/f9cc35ebad82753e9c86de322ea5c76a9001c7e2/wp-admin/setup-config.php#L216-L230
* (However, using "example username" and "example password" in your database is strongly discouraged.  Please use strong, random credentials!)
*/

/** Database hostname */
define( 'DB_HOST', getenv_docker('WORDPRESS_DB_HOST', 'mysql') );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', getenv_docker('WORDPRESS_DB_CHARSET', 'utf8') );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', getenv_docker('WORDPRESS_DB_COLLATE', '') );

/**#@+
* Authentication unique keys and salts.
*
* Change these to different unique phrases! You can generate these using
* the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
*
* You can change these at any point in time to invalidate all existing cookies.
* This will force all users to have to log in again.
*
* @since 2.6.0
*/
define( 'AUTH_KEY',         getenv_docker('WORDPRESS_AUTH_KEY',         '036f69e6cac545dc67b76f90181a2a5ff3ac8539') );
define( 'SECURE_AUTH_KEY',  getenv_docker('WORDPRESS_SECURE_AUTH_KEY',  '6b2e93cec23dded77bc79eeb4a671dd5b25bb7f6') );
define( 'LOGGED_IN_KEY',    getenv_docker('WORDPRESS_LOGGED_IN_KEY',    '2411beaf33cb1107ac7952ede192850bdfc28c88') );
define( 'NONCE_KEY',        getenv_docker('WORDPRESS_NONCE_KEY',        '18ed695eb63ab0441588403328de9e6088fe3e8e') );
define( 'AUTH_SALT',        getenv_docker('WORDPRESS_AUTH_SALT',        'f06a3ad240a0da3b74e77751746e0504219d03fe') );
define( 'SECURE_AUTH_SALT', getenv_docker('WORDPRESS_SECURE_AUTH_SALT', '4460552c50dab518f39466fe0597091985e13731') );
define( 'LOGGED_IN_SALT',   getenv_docker('WORDPRESS_LOGGED_IN_SALT',   '38403cc0dd102a176f2717aec20951cd20c3b7c3') );
define( 'NONCE_SALT',       getenv_docker('WORDPRESS_NONCE_SALT',       '02a9c9a072b277a31bbcb648459c120a10f2894d') );
// (See also https://wordpress.stackexchange.com/a/152905/199287)

/**#@-*/

/**
* WordPress database table prefix.
*
* You can have multiple installations in one database if you give each
* a unique prefix. Only numbers, letters, and underscores please!
*/
$table_prefix = getenv_docker('WORDPRESS_TABLE_PREFIX', 'wp_');

/**
* For developers: WordPress debugging mode.
*
* Change this to true to enable the display of notices during development.
* It is strongly recommended that plugin and theme developers use WP_DEBUG
* in their development environments.
*
* For information on other constants that can be used for debugging,
* visit the documentation.
*
* @link https://wordpress.org/support/article/debugging-in-wordpress/
*/
define( 'WP_DEBUG', !!getenv_docker('WORDPRESS_DEBUG', '') );

/* Add any custom values between this line and the "stop editing" line. */

// If we're behind a proxy server and using HTTPS, we need to alert WordPress of that fact
// see also https://wordpress.org/support/article/administration-over-ssl/#using-a-reverse-proxy
if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && strpos($_SERVER['HTTP_X_FORWARDED_PROTO'], 'https') !== false) {
    $_SERVER['HTTPS'] = 'on';
}
// (we include this by default because reverse proxying is extremely common in container environments)

if ($configExtra = getenv_docker('WORDPRESS_CONFIG_EXTRA', '')) {
    eval($configExtra);
}

/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
    define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
"""
        Path(deployToDir).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(deployToDir, "wp-config.php"), "w") as f:
            f.write(wp_config)

        php_info = """<?php phpinfo();"""
        with open(os.path.join(deployToDir, "info123321.php"), "w") as f:
            f.write(php_info)
