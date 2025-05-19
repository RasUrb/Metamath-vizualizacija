from browser import document as doc 
from browser import document as svg, html, window 
import browser.html as html
import browser.svg as svg
import base64
    
def bind_download_buttons(diagram):
    
    def build_svg(diagram):
        svg_elem  = svg.svg()
        min_x, min_y, total_width, total_height = diagram.get_total_bounds()
        svg_elem .attrs["width"] = f"{int(total_width)}px"
        svg_elem .attrs["height"] = f"{int(total_height)}px"
        svg_elem .attrs["viewBox"] = f"{min_x} {min_y} {total_width} {total_height}"
        #print(f"svg_elem: {svg_elem .attrs["viewBox"]}")

        for rect in diagram.rectangle:
            svg_elem  <= rect.rect_svg.cloneNode(True)

        for text in diagram.text:
            svg_elem <= text.text_svg.cloneNode(True)
        return svg_elem 
    
    
    def get_svg_blob():
        svg_elem  = build_svg(diagram)

        # Serialize SVG to string
        serializer = window.XMLSerializer.new()
        my_svg_data = serializer.serializeToString(svg_elem)

        # Create a Blob
        blob = window.Blob.new([my_svg_data], { "type": "image/svg+xml" })
        return blob

    def save_as_svg(event):
        blob = get_svg_blob()

        file_name = window.prompt("Įveskite SVG failo pavadinimą:", "vaizdas")
        if file_name:
            url = window.URL.createObjectURL(blob)
            a = doc.createElement("a")
            a.href = url
            a.download = file_name
            doc.body.appendChild(a)
            a.click()
            doc.body.removeChild(a)
            window.URL.revokeObjectURL(url) 

    def save_as_png(event):
        svg_elem = build_svg(diagram)  # tavo SVG objektas
        svg_string = svg_elem.outerHTML
        if "xmlns=" not in svg_string:
            svg_string = svg_string.replace(
                "<svg ",
                '<svg xmlns="http://www.w3.org/2000/svg" ',
                1
            )
        # Konvertuoti SVG į base64
        svg_base64 = base64.b64encode(svg_string.encode('utf-8')).decode('utf-8')
        data_uri = f"data:image/svg+xml;base64,{svg_base64}"
        img = html.IMG(src=data_uri)

        def onload(ev):
        # Naudojam viewBox, jei nėra width/height arba jei klaidingi
            view_box = svg_elem.attrs.get("viewBox")
            if view_box:
                parts = view_box.split()
                try:
                    canvas_width = int(float(parts[2]))  # viewBox width
                    canvas_height = int(float(parts[3])) # viewBox height
                except (IndexError, ValueError):
                    canvas_width = 800
                    canvas_height = 600
            else:
                # fallback
                canvas_width = 800
                canvas_height = 600
            #print(f"Canvas dydis: {canvas_width} x {canvas_height}")
            canvas = doc.createElement("canvas")
            canvas.setAttribute("width", str(canvas_width))
            canvas.setAttribute("height", str(canvas_height))

            ctx = canvas.getContext("2d")
            ctx.clearRect(0, 0, canvas.width, canvas.height)
            ctx.drawImage(img, 0, 0)

            png_data = canvas.toDataURL("image/png")

            file_name = window.prompt("Įveskite PNG failo pavadinimą:", "vaizdas.png")
            if file_name:
                a = doc.createElement("a")
                a.href = png_data
                a.download = file_name
                doc.body.appendChild(a)
                a.click()
                doc.body.removeChild(a)
            
            for canvas in doc.select("canvas"):
                canvas.remove() 
        img.bind("load", onload)
        for img in doc.select(".temp-img"):
            img.remove()
        #img.bind("load", on_img_load)
    # Bindinam jau esančius mygtukus
    # Pririšam save_as_svg prie  mygtuko
    old_btn = doc["downloadSVG"]
    new_btn = old_btn.cloneNode(True)
    old_btn.parent.replaceChild(new_btn, old_btn)
    new_btn.bind("click", save_as_svg)

    # Pririšam save_as_png prie downloadPng mygtuko
    old_btn = doc["downloadPng"]
    new_btn = old_btn.cloneNode(True)
    old_btn.parent.replaceChild(new_btn, old_btn)
    new_btn.bind("click", save_as_png)
