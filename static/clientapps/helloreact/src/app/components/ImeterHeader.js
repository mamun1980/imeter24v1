import React from "react";


export class ImeterHeader extends React.Component {
    
    render() {

      return (
        
            <table className="mdl-data-table mdl-js-data-table mdl-data-table--selectable mdl-shadow--2dp">
              <thead>
                <tr>
                  <th >Site ID</th>
                  <th className="mdl-data-table__cell--non-numeric">Location Details</th>
                  
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>25</td>
                  <td className="mdl-data-table__cell--non-numeric">Acrylic (Transparent)</td>
                  
                </tr>
                <tr>
                  <td>50</td>
                  <td className="mdl-data-table__cell--non-numeric">Plywood (Birch)</td>
                  
                </tr>
                <tr>
                  <td>10</td>
                  <td className="mdl-data-table__cell--non-numeric">Laminate (Gold on Blue)</td>
                  
                </tr>
              </tbody>
            </table>

      );
    }
}
