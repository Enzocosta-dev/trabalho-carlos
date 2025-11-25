from flask import Flask, jsonify, request
from flask_cors import CORS
from modelo import Usuario, Propriedade, Reserva, SessionLocal

# ----------------- FLASK -----------------
app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer origem

# ----------------- FUNÇÃO AUXILIAR -----------------
def get_session():
    """Cria uma sessão segura"""
    return SessionLocal()

# ----------------- HOME -----------------
@app.route("/")
def home():
    return jsonify({"mensagem": "API Flask + SQL Server conectada!"})

# ----------------- USUÁRIOS -----------------
@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    session = get_session()
    try:
        usuarios = session.query(Usuario).all()
        return jsonify([u.to_dict() for u in usuarios])
    finally:
        session.close()

@app.route("/usuarios", methods=["POST"])
def adicionar_usuario():
    session = get_session()
    try:
        dados = request.get_json()
        novo = Usuario(
            NOME=dados["NOME"],
            CPF=dados["CPF"],
            TELEFONE=dados.get("TELEFONE"),
            EMAIL=dados.get("EMAIL"),
            SENHA=dados["SENHA"],
            NIVEL=dados.get("NIVEL", "cliente"),
            FOTO=dados.get("FOTO")
        )
        session.add(novo)
        session.commit()
        return jsonify({"mensagem": "Usuário adicionado!"})
    except Exception as e:
        session.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        session.close()

@app.route("/usuarios/<int:id>", methods=["PUT"])
def atualizar_usuario(id):
    session = get_session()
    try:
        dados = request.get_json()
        usuario = session.query(Usuario).filter_by(ID=id).first()
        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404
        if "NIVEL" in dados:
            usuario.NIVEL = dados["NIVEL"]
        session.commit()
        return jsonify({"mensagem": "Usuário atualizado com sucesso"})
    except Exception as e:
        session.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        session.close()

@app.route("/usuarios/<int:id>", methods=["DELETE"])
def deletar_usuario(id):
    session = get_session()
    try:
        usuario = session.query(Usuario).filter_by(ID=id).first()
        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404
        for reserva in usuario.reservas:
            session.delete(reserva)
        for prop in usuario.propriedades:
            session.delete(prop)
        session.delete(usuario)
        session.commit()
        return jsonify({"mensagem": "Usuário excluído com sucesso"})
    except Exception as e:
        session.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        session.close()

# ----------------- LOGIN -----------------
@app.route("/login", methods=["POST"])
def login():
    session = get_session()
    try:
        dados = request.get_json()
        email = dados.get("EMAIL", "").strip()
        senha = dados.get("SENHA", "").strip()

        # Busca ignorando maiúsculas/minúsculas e espaços extras
        usuario = session.query(Usuario).filter(Usuario.EMAIL.ilike(email)).first()
        if usuario and usuario.SENHA.strip() == senha:
            return jsonify({"mensagem": "Login realizado!", "usuario": usuario.to_dict()})
        return jsonify({"erro": "Email ou senha inválidos"}), 401
    finally:
        session.close()

# ----------------- PROPRIEDADES -----------------
@app.route("/propriedades", methods=["GET"])
def listar_propriedades():
    session = get_session()
    try:
        props = session.query(Propriedade).all()
        return jsonify([p.to_dict() for p in props])
    finally:
        session.close()

@app.route("/propriedades", methods=["POST"])
def adicionar_propriedade():
    session = get_session()
    try:
        dados = request.get_json()
        usuario_id = dados.get("USUARIO_ID")  # Recebido do front-end como usuário logado

        nova = Propriedade(
            LOCAL=dados["LOCAL"],
            PRECO=dados["PRECO"],
            QUARTOS=dados["QUARTOS"],
            TAMANHO=dados["TAMANHO"],
            IMAGEM=dados["IMAGEM"],
            USUARIO_ID=usuario_id
        )
        session.add(nova)
        session.commit()
        return jsonify({"mensagem": "Propriedade adicionada!"})
    except Exception as e:
        session.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        session.close()

@app.route("/propriedades/<int:id>", methods=["PUT"])
def atualizar_propriedade(id):
    session = get_session()
    try:
        dados = request.get_json()
        prop = session.query(Propriedade).filter_by(ID=id).first()
        if not prop:
            return jsonify({"erro": "Propriedade não encontrada"}), 404
        for campo in ["LOCAL", "PRECO", "QUARTOS", "TAMANHO", "IMAGEM"]:
            if campo in dados:
                setattr(prop, campo, dados[campo])
        session.commit()
        return jsonify({"mensagem": "Propriedade atualizada!"})
    except Exception as e:
        session.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        session.close()

@app.route("/propriedades/<int:id>", methods=["DELETE"])
def deletar_propriedade(id):
    session = get_session()
    try:
        prop = session.query(Propriedade).filter_by(ID=id).first()
        if not prop:
            return jsonify({"erro": "Propriedade não encontrada"}), 404
        for reserva in prop.reservas:
            session.delete(reserva)
        session.delete(prop)
        session.commit()
        return jsonify({"mensagem": "Propriedade excluída com sucesso"})
    except Exception as e:
        session.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        session.close()

# ----------------- RESERVAS -----------------
@app.route("/reservas", methods=["GET"])
def listar_reservas():
    session = get_session()
    try:
        reservas = session.query(Reserva).all()
        return jsonify([r.to_dict() for r in reservas])
    finally:
        session.close()

@app.route("/reservas", methods=["POST"])
def adicionar_reserva():
    session = get_session()
    try:
        dados = request.get_json()
        nova = Reserva(
            USUARIO_ID=dados["USUARIO_ID"],
            PROPRIEDADE_ID=dados["PROPRIEDADE_ID"],
            PRECO=dados["PRECO"],
            DATA_RESERVA=dados["DATA_RESERVA"],
            FIM_RESERVA=dados.get("FIM_RESERVA")
        )
        session.add(nova)
        session.commit()
        return jsonify({"mensagem": "Reserva criada!"})
    except Exception as e:
        session.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        session.close()

# ----------------- RODAR API -----------------
if __name__ == "__main__":
    app.run(debug=True)
