#!/usr/bin/env python
# -*- coding: utf-8 -*-

#       _                              
#      | |                             
#    __| |_ __ ___  __ _ _ __ ___  ___ 
#   / _` | '__/ _ \/ _` | '_ ` _ \/ __|
#  | (_| | | |  __/ (_| | | | | | \__ \
#   \__,_|_|  \___|\__,_|_| |_| |_|___/ .
#
# A 'Fog Creek'–inspired demo by Kenneth Reitz™

import os
from flask import Flask, request, render_template, jsonify,send_file
import test




#from PIL import Image, ImageDraw, ImageFont
import io
from PIL import Image, ImageDraw, ImageFont





def converter_hex_para_rgba(cor_hex):
    # Remover o caractere '#' se estiver presente
    if cor_hex.startswith('#'):
        cor_hex = cor_hex[1:]

    # Verificar se o valor de transparência está presente na cor hexadecimal
    if len(cor_hex) == 8:
        a = int(cor_hex[6:8], 16)
    else:
        # Definir o valor de transparência como 255 (opaco) por padrão
        a = 255

    # Converter o valor hexadecimal em valores RGB
    r = int(cor_hex[0:2], 16)
    g = int(cor_hex[2:4], 16)
    b = int(cor_hex[4:6], 16)

    # Retornar o conjunto de valores RGBA
    return (r, g, b, a)



import io
from PIL import Image, ImageDraw, ImageFont
import textwrap

import io
from PIL import Image, ImageDraw, ImageFont
import textwrap

import io
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
from PIL import Image, ImageDraw, ImageFont
import textwrap

import textwrap



def criar_imagem_com_texto(texto, cor_texto=(255, 255, 255), margem=32, font_size=20):
    # Configurações da imagem
    cor_fundo = (0, 0, 0, 0)
    tamanho_fonte = font_size
    espacamento_linha = 10

    # Criar um objeto de fonte com o tamanho especificado
    fonte = ImageFont.truetype("./Invisible-ExtraBold.otf", size=tamanho_fonte)
   
    # Dividir o texto em linhas com base em um comprimento máximo
    linhas = []
    for linha in texto.splitlines():
        linhas.extend(textwrap.wrap(linha, width=50))  # Defina o limite de largura desejado

    # Calcular o tamanho necessário para o texto
    tamanho_texto = (0, 0)
    for linha in linhas:
        tamanho_linha = fonte.getsize(linha)
        tamanho_texto = (
            max(tamanho_texto[0], tamanho_linha[0]),
            tamanho_texto[1] + tamanho_linha[1] + espacamento_linha
        )

    # Criar uma nova imagem com base no tamanho do texto
    imagem = Image.new("RGBA", (tamanho_texto[0]+margem*2, tamanho_texto[1]+margem), cor_fundo)

    # Criar um objeto de desenho
    desenho = ImageDraw.Draw(imagem)

    # Definir a posição inicial para desenhar o texto
    posicao = (0, 0)

    # Desenhar cada linha do texto na imagem
    for linha in linhas:
        tamanho_linha = fonte.getsize(linha)
        desenho.text((posicao[0] + margem, posicao[1] + margem), linha, fill=cor_texto, font=fonte)
        posicao = (posicao[0], posicao[1] + tamanho_linha[1] + espacamento_linha)  # Avançar para a próxima linha

    # Retornar a imagem
    buffer = io.BytesIO()
    imagem.save(buffer, format="PNG")
    buffer.seek(0)

    # Retornar o conteúdo da imagem
    return buffer.getvalue()



# Support for gomix's 'front-end' and 'back-end' UI.
app = Flask(__name__, static_folder='public', template_folder='views')



# Set the app secret key from the secret environment variables.
app.secret = os.environ.get('SECRET')

# Dream database. Store dreams in memory for now. 
DREAMS = ['Python. Python, everywhere.']


@app.after_request
def apply_kr_hello(response):
    """Adds some headers to all responses."""
  
    # Made by Kenneth Reitz. 
    if 'MADE_BY' in os.environ:
        response.headers["X-Was-Here"] = os.environ.get('MADE_BY')
    
    # Powered by Flask. 
    response.headers["X-Powered-By"] = os.environ.get('POWERED_BY')
    return response


  
  
  
  
@app.route("/generate")
def retornar_imagem():
    if ( "text" in request.args):
      color = "#ff0000"
      font_size = 20
      margin = 6
      if "color" in request.args:
        color = request.args["color"]
      if "font_size" in request.args:
        font_size = int(request.args["font_size"])
      if "margin" in request.args:
        margin = int(request.args["margin"])
      print(color)
      
      
      conteudo_imagem = criar_imagem_com_texto(request.args["text"], converter_hex_para_rgba(color), margin, font_size)
      return send_file(io.BytesIO(conteudo_imagem), mimetype="image/png")
    return "fail"

  
@app.route('/')
def homepage():
    return render_template('index.html')
  


if __name__ == '__main__':
    app.run()
    
