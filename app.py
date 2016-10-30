#!/usr/bin/env python3

import connexion
import os

if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.add_api('swagger.yaml', arguments={'title': 'Share your Tsurai'})
    app.run(host='0.0.0.0',port=os.environ.get('PORT',8080))
