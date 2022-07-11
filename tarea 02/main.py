from flask import Flask, render_template, request, flash
import time
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gatitos peludos'

user_container = []

db = sqlite3.connect('login.db', check_same_thread=False)
cursor = db.cursor()

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def iniciar_sesion():
    usuario = request.form['usuario']
    contraseña = request.form['password']
    
    cursor.execute(f'SELECT contraseña FROM datos WHERE usuario="{usuario}"')
    database_passw = cursor.fetchall()
    
    isPasswordCorrect = False
    hasError = 'False'
    for i in database_passw:
        for userPassword in i:
            if userPassword == contraseña:
                isPasswordCorrect = True
                hasError = 'True'
                if hasError == 'True':
                    cursor.execute(f'SELECT nombre FROM datos WHERE usuario="{usuario}"')
                    database_name = cursor.fetchone()
                    nombre = ''
                    for a in database_name:
                        nombres = nombre.join(a)
                        flash(f'haz iniciado sesión correctamente {nombres}', 'success')
                
            elif contraseña not in userPassword:
                isPasswordCorrect = True
                flash('la contraseña ingresada no es correcta', 'danger')
                
        if isPasswordCorrect == True:
            break
    if isPasswordCorrect == False:
        if hasError == 'False':
            flash('error, este usuario no existe!', 'danger')
            
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('registrarse.html')

@app.route('/registrarse', methods=['POST'])
def registrarse():
    nombre = request.form['nombre']
    usuario = request.form['usuario']
    correo = request.form['correo']
    numero = request.form['numero']
    contraseña = request.form['contraseña']
    
    registro = nombre, usuario, correo, numero, contraseña
    
    data_correo = cursor.execute('SELECT correo FROM datos')
    database_correo = data_correo.fetchall()
    
    data_usuario = cursor.execute('SELECT usuario FROM datos')
    database_usuario = data_usuario.fetchall()
    
    data_numero = cursor.execute('SELECT numero FROM datos')
    database_numero = data_numero.fetchall()
    
    valor = True
    valor2 = 'True'
    
    for x in database_correo:
        for y in x:
            if y == correo:
                valor = False
                valor2 = 'False'
                
                if valor2 == 'False':
                    flash('El correo ingresado ya ha sido utilizado', 'danger')
        
        if valor == False:
            break
    if valor == True:
        valor3 = False
        for i in database_usuario:
            for c in i:
                if c == usuario:
                    valor3 = True
                    flash('El usuario ingresado ya existe!', 'danger')
            
            if valor3 == True:
                break
        
        if valor3 == False:
            valor4 = False
            for s in database_numero:
                for z in s:
                    if z == numero:
                        valor4 = True
                        flash('El numero de telefono ingresado ya existe!', 'danger')

                if valor4 == True:
                    break
            if valor4 == False:
                cursor.execute('INSERT into datos(nombre, usuario, correo, numero, contraseña) VALUES(?, ?, ?, ?, ?)', registro)
                db.commit()
                flash('Te haz registrado satisfactoriamente!', 'success')
                time.sleep(2)
                return render_template('index.html')
    
    return render_template('registrarse.html')

@app.route('/contraseña')
def contraseña():
    return render_template('password.html')

@app.route('/autentificacion', methods=['POST'])
def autentificacion():
    usuario = request.form['usuario']
    numero = request.form['numero']
    
    user = cursor.execute(f'SELECT numero FROM datos WHERE usuario= "{usuario}"')
    data_user = user.fetchall()
    
    valor = False
    for x in data_user:
        for y in x:
            if y == numero:
                valor = True
                flash('Numero ingresado con exito', 'success')
                user_container.append(usuario)
                time.sleep(3)
                return render_template('cambiarcontraseña.html')
        
        if valor == True:
            break
    if valor == False:
        flash('El numero ingresado no es correcto', 'danger')
    
    return render_template('password.html')

@app.route('/cambiarcontraseña', methods=['POST'])
def cambiar_contraseña():
    usuario = request.form['usuario']
    nuevacontraseña = request.form['nuevacontraseña']
    confirmar_contraseña = request.form['confirmarcontraseña']
    print(user_container)
    
    date_user = cursor.execute('SELECT usuario FROM datos')
    datos = date_user.fetchall()
    valor = False
    valor2 = True
    for e in datos:
        for valores in e:
            if valores == usuario:
                valor = True
                
                date_passw = cursor.execute(f'SELECT contraseña FROM datos WHERE usuario="{usuario}"')
                user_passw = date_passw.fetchone()
                 
                passw = ''
                for x in user_passw:
                    passw = passw.join(x)
                

                    if confirmar_contraseña == passw:
                        flash('esta contraseña ya la utilizaste, usa otra!', 'danger')
                        valor2 = False
                        
                    elif valor2 == True:
                        if nuevacontraseña == confirmar_contraseña:
                            cursor.execute(f'UPDATE datos SET contraseña="{confirmar_contraseña}" WHERE usuario="{usuario}"')
                            db.commit()
                            flash('contraseña cambiada con exito!', 'success')
                            time.sleep(2)
                            return render_template('index.html')
                        
                        else:
                            flash('las contraseñas no coinciden', 'danger')
            else:
                flash('el usuario ingresado no es correcto', 'danger')
        
        if valor == True:
            break
               
    return render_template('cambiarcontraseña.html')
                    
    

if __name__=='__main__':
    app.run(debug=True, port=400)