.. vpsc documentation master file, created by
   sphinx-quickstart on Wed Jan  3 14:12:21 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

vpscのドキュメントへようこそ！

さくらのVPSの非公式クライアントです。
`さくらのVPS API <https://manual.sakura.ad.jp/vps/api/index.html>`_ をコマンドラインもしくはPython上で容易に扱えるようにすることを目標に作っています。

利用可能コマンドや関数に関しては :doc:`vpsc` を参照してください。


================================


利用方法
========================

インストール
----------------

.. code-block:: bash

   $ pip install vpsc

環境変数の設定
----------------

利用するためにはAPIキーの設定が最低限必要です

.. code-block:: bash

   $ export VPS_API_KEY=xxx
   // optional
   $ export VPS_HOST="https://secure.sakura.ad.jp/vps/api/v7"

もしくは `~/.vpsc` に設定を入れます

.. code-block:: bash

   VPS_API_KEY=xxx
   // optional
   VPS_HOST="https://secure.sakura.ad.jp/vps/api/v7"


Todo
========================
* エラーハンドリング
* コマンドの追加

その他
========================
気になることがありましたら、リポジトリにissueやPRを投げてください！

================================

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   vpsc


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
