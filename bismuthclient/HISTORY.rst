=======
History
=======

0.0.1 (2018-11-17)
------------------

* First release on PyPI.

0.0.2 (2018-11-20)
------------------

* Alpha release

0.0.21 (2018-11-26)
-------------------

* Added features, still Alpha

0.0.22 (2018-11-30)
-------------------

* Added features, still Alpha

0.0.23 (2018-11-30)
-------------------

* Fix AmountFormatter

0.0.24 (2018-12-02)
-------------------

* Bismuth Util Class
* Incremental updates

0.0.25 (2018-12-02)
-------------------

* Fix AmountFormatter (again)

0.0.26 (2018-12-05)
-------------------

* Fix Send with data

0.0.27 (2018-12-09)
-------------------

* Small improvements

0.0.28 (2018-12-10)
-------------------

* Small improvements


0.0.29 (2018-12-11)
-------------------

* Embed simplecrypt, removes need for old and unmaintained pycrypto and simplecrypt modules.
* Add missing "requests" dependencies

0.0.30 (2018-12-18)
-------------------

* Removed debug log
* BismuthClient, user_subdir now is a static method

0.0.31 (2019-01-19)
-------------------

* BismuthMultiWallet class
* Various fixes and addition to support Tornado Wallet

0.0.32 (2019-01-19)
-------------------

* Bugfix

0.0.33 (2019-01-19)
-------------------

* Bugfix again

0.0.34 (2019-03-07)
-------------------

* Bugfix

0.0.35 (2019-03-09)
-------------------

* More info from API
* Full server list property with load and height
* refresh_server_list method

0.0.36 (2019-03-10)
-------------------

* Edit Address labels


0.0.37 (2019-03-14)
-------------------

* Fix labels with encrypted wallets

0.0.38 (2019-03-14)
-------------------

* Multi level encryption support for faster operations on encrypted wallets.

0.0.39 (2019-03-14)
-------------------

* Fix leaking info

0.0.40 (2019-05-03)
-------------------

* Addons to support new wallet functions.
* import encrypted wallet.der
* reject empty messages tx to exchanges
* reduce verbosity

0.0.41 (2019-05-04)
-------------------

* First support for alias functions
* cached alias results

0.0.42 (2019-05-12)
-------------------

More feedback on failed tx submission

0.0.43 (2019-05-18)
-------------------

Fixed encrypted wallet.der loading

0.0.44 (2019-05-20)
-------------------

Support for message encryption/decryption and pubkey retrieval

0.0.45 (2019-06-27)
-------------------

Support for new addresses schemes

0.0.46 (2019-06-28)
-------------------

Support for optional mempool txs in last transactions.

0.0.47 (2019-07-14)
-------------------

Fixes by @Endogen, alias support

0.0.48 (2019-09-30)
-------------------

First support for other crypto schemes, include polysign.

0.0.49 (2019-10-16)
-------------------

Fix single wallet operations

0.0.50 (2020-05-09)
-------------------

Merge dev branch, several new features to doc
Update to supply calculation

0.0.51 (2021-04-18)
-------------------

Support for very old style privkey.der wallets
New feature: sublimate and condensate utils, to split privkveys into several chunks.
All chunks are then needed to rebuild the key.

