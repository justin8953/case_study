import React, {useState , useEffect} from 'react';
import axios from "axios";
import { Table, Container } from 'react-bootstrap';

function toThousands(num) {
   return (num || 0).toString().replace(/(\d)(?=(?:\d{3})+$)/g, '$1,');
}

const FundSummary=(props)=>{
   const [investment, setInvestment] = useState([])
   const [funds, setFunds] = useState([])
   
   useEffect(()=>{
      //  Get fund name for table header
      var url = "http://127.0.0.1:8000/funds/"
      var fundNum = 0
      axios.get(url).then((res)=>{
         var arr = []
         res.data.forEach(element => {
            arr.push(element.name)
         });
         setFunds(arr)
         fundNum = arr.length
      }).catch((err)=>{
         console.log(err)
      })
      // get dash board summary
      var summaryUrl = "http://127.0.0.1:8000/summary/"
      axios.get(summaryUrl).then((res)=>{
         var arr = []
         res.data.forEach(element => {
            var row = []
            var fund = []
            var i;
            for (i=0; i<fundNum; i++){
               fund.push('-')
            }
            row.push(element.date)
            row.push(element.id)
            element.funds.forEach(e =>{
               fund[e.fund-1] = toThousands(e.amount)
            })
            console.log(fund)
            arr.push(row.concat(fund))
         });
         setInvestment(arr)
      }).catch((err)=>{
         console.log(err)
      })
   }, [props.funds, props.investment, props.numOfFunds])
   return (
      <Container className="mt-3">
         <Table>
            <thead>
               <tr>
                  <th>Date</th>
                  <th>Call #</th>
                  {funds.map(item=><th>{item}</th>)}
               </tr>
            </thead>
            <tbody>
               {investment.map(ele=>
               <tr>{ ele.map(e=> 
                  <th>{e}</th>
                  )}
               </tr>
               )}
            </tbody>
         </Table>
      </Container>
   );
}
export default FundSummary 