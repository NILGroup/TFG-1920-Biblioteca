//
//  EmailViewCell.swift
//  Janet
//
//  Created by Miguel Ángel on 23/05/2020.
//  Copyright © 2020 Mauri. All rights reserved.
//  MIT License
//
//  Copyright (c) 2019 Mauricio Abbati Loureiro - Jose Luis Moreno Varillas
//
//  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
//
//  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
//
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
//

import UIKit

//Clase para un globo de conversación con un telefóno.
class EmailViewCell: TableViewCell {
    
    @IBOutlet weak var Email: UILabel!
    @IBOutlet weak var View: UIView!
    @IBOutlet weak var Library: UILabel!
    
    //Inicializa los atributos de la clase.
    override func setDatos(info: Globos) {
        
        self.message.text = info.getRespuesta()
        self.message.textAlignment = .left
        self.message.sizeToFit()
        self.cambiarBurbuja(info: .Bot)
        
        //Establece un enlace en la vista para hacer una llamada a través de la aplicación teléfono del sistema.
        View.isUserInteractionEnabled = true
        let tap = UITapGestureRecognizer(target: self, action: #selector(viewPhoneTapped))
        View.addGestureRecognizer(tap)
        
        Email.text = String(info.getEmail())
        Library.text = info.getLibrary()
    }
    
    //Establece un enlace en la vista para hacer una llamada a través de la aplicación teléfono del sistema.
    @objc private func viewPhoneTapped(sender: UITapGestureRecognizer) {
        guard let number = URL(string: "mailto://" + Email.text!) else { return }
        UIApplication.shared.open(number)
    }
    
}

