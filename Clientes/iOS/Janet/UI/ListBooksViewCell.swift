//
//  ListBooksViewCell.swift
//  [TFG] Asistente virtual para servicios de la biblioteca de la UCM - Codename "Janet"
//
//  Created by Mauri on 11/12/2018.
//  Copyright © 2018 Mauricio Abbati Loureiro - Jose Luis Moreno Varillas. All rights reserved.
//

import UIKit

class ListBooksViewCell: TableViewCell {

    @IBOutlet weak var View1: UIView!
    @IBOutlet weak var titleLabel1: UILabel!
    @IBOutlet weak var coverart1: UIImageView!
    @IBOutlet weak var authorLabel1: UILabel!
    
    @IBOutlet weak var View2: UIView!
    @IBOutlet weak var titleLabel2: UILabel!
    @IBOutlet weak var coverart2: UIImageView!
    @IBOutlet weak var authorLabel2: UILabel!
    
    @IBOutlet weak var View3: UIView!
    @IBOutlet weak var titleLabel3: UILabel!
    @IBOutlet weak var coverart3: UIImageView!
    @IBOutlet weak var authorLabel3: UILabel!
    
    var list: [Globos]? = nil
    
    override func setDatos(info: Globos) {
        
        self.list = info.getlist()
        
        View1.isUserInteractionEnabled = true
        let tap1 = UITapGestureRecognizer(target: self, action: #selector(view1Tapped))
        View1.addGestureRecognizer(tap1)
        
        View2.isUserInteractionEnabled = true
        let tap2 = UITapGestureRecognizer(target: self, action: #selector(view2Tapped))
        View2.addGestureRecognizer(tap2)
        
        View3.isUserInteractionEnabled = true
        let tap3 = UITapGestureRecognizer(target: self, action: #selector(view3Tapped))
        View3.addGestureRecognizer(tap3)
        
        self.message.text = "Janet: " + info.getRespuesta()
        self.message.textAlignment = .left
        self.message.sizeToFit()
        self.cambiarBurbuja(info: .Bot)
        
        let list = info.getlist()
        
        for i in 0..<3 {
            if (i == 0) {
                var image: UIImage?
                
                if (coverart1.image == nil) {
                    let url = NSURL(string: list[i].getImagen())! as URL
                    if let imageData: NSData = NSData(contentsOf: url) {
                        image = UIImage(data: imageData as Data)
                        if (image?.size.width == 1) {
                            image = nil
                        }
                    }
                    coverart1.image = image
                }
                
                titleLabel1.text = list[i].getTitle()
                authorLabel1.text = list[i].getAuthor()
            } else if (i == 1) {
                var image: UIImage?
                
                if (coverart2.image == nil) {
                    let url = NSURL(string: list[i].getImagen())! as URL
                    if let imageData: NSData = NSData(contentsOf: url) {
                        image = UIImage(data: imageData as Data)
                        if (image?.size.width == 1) {
                            image = nil
                        }
                    }
                    coverart2.image = image
                }
                
                titleLabel2.text = list[i].getTitle()
                authorLabel2.text = list[i].getAuthor()
            } else {
                var image: UIImage?
                
                if (coverart3.image == nil) {
                    let url = NSURL(string: list[i].getImagen())! as URL
                    if let imageData: NSData = NSData(contentsOf: url) {
                        image = UIImage(data: imageData as Data)
                        if (image?.size.width == 1) {
                            image = nil
                        }
                    }
                    coverart3.image = image
                }
                
                titleLabel3.text = list[i].getTitle()
                authorLabel3.text = list[i].getAuthor()
            }
        }
        
        
    }
    
    @objc private func view1Tapped(sender: UITapGestureRecognizer) {
        print("bigButton1Tapped")
        let dict = ["tipo": "oclc", "peticion": self.list![0].getCodOCLC()] as [String : Any]
        NotificationCenter.default.post(name: NSNotification.Name(rawValue: "view1Tapped"), object: nil, userInfo: dict)
    }
    
    @objc private func view2Tapped(sender: UITapGestureRecognizer) {
        print("bigButton2Tapped")
        let dict = ["tipo": "oclc", "peticion": self.list![1].getCodOCLC()] as [String : Any]
        NotificationCenter.default.post(name: NSNotification.Name(rawValue: "view1Tapped"), object: nil, userInfo: dict)
    }
    
    @objc private func view3Tapped(sender: UITapGestureRecognizer) {
        print("bigButton3Tapped")
        let dict = ["tipo": "oclc", "peticion": self.list![2].getCodOCLC()] as [String : Any]
        NotificationCenter.default.post(name: NSNotification.Name(rawValue: "view1Tapped"), object: nil, userInfo: dict)
    }
}
