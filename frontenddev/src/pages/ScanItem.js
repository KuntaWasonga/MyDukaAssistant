//This contains code for the landing page of the web application
import React, { } from "react";
//import Dynamsoft from 'dynamsoft-javascript-barcode';

import { Link } from 'react-router-dom';

export default function ScanItem() {
  //let peace = (async () => {
    //let scanner = await Dynamsoft.DBR.BarcodeScanner.createInstance();
    //await scanner.setUIElement(document.getElementById('div-ui-container'));
    //scanner.onFrameRead = results => {
    //  console.log(results);
  //  };
//    scanner.onUniqueRead = (txt, result) => {
      //alert(txt);
    //};
  //  await scanner.show();
//  })();

  return (
    <div id="div-ui-container" style="width:100%;height:100%;">
      <div class="dce-video-container" style="position:relative;width:100%;height:500px;">
        <button onclick="peace();">WOW</button>
      </div>
    </div>
  );
}

//<script src="https://cdn.jsdelivr.net/npm/dynamsoft-javascript-barcode@9.6.20/dist/dbr.js"></script>
