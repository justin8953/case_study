import React, {useState, useEffect} from 'react';
import {Form, Button, Container, Table} from 'react-bootstrap';
import axios from "axios";

function toThousands(num) {
  return (num || 0).toString().replace(/(\d)(?=(?:\d{3})+$)/g, '$1,');
}

const Callform = (props) =>{
  const [date, setDate] = useState("");
  const [investName, setInvestName] = useState("");
  const [callAmount, setRequirement] = useState(0);
  const [temporttable, setTemporttable] = useState([])
  const [calculateTable, setCalculateTable] = useState([])
  const [btnActive, setActive] = useState(true)
  const [fundInvestList, setList] = useState([])
  const [callId, setCallId] = useState(0)
  const count = ()=>{
    //  Get Current Call id
    var url = "http://127.0.0.1:8000/calls/"
    axios.get(url).then((res)=>{
      var tail = res.data.length - 1
      setCallId(res.data[tail].id)
    }).catch(err=>{
      console.log(err)
    })
    //  New call requirement
    var currentRequirement = callAmount
    //  Empty Data list for calculation table
    var newarray = []
    //  Empty Data list for post the investment at each fund 
    var newarr2 = []

    temporttable.forEach(e =>{
      //  dict for each row in calculation table
      var newRow = {}
      //  Initial total drop down
      var totalDropDown = 0
      //  Initial after total drop down
      var afterTotal = e.notice
       
      if(currentRequirement > 0 && currentRequirement> e.notice){
        
        totalDropDown = e.notice
        afterTotal = 0
        newRow.commit_id = e.commit_id
        
        if(totalDropDown!==0){
          newRow.fund_id = e.fund_id
          newRow.invest_amount = totalDropDown
          newarr2.push(newRow)
        }
        
        currentRequirement = currentRequirement- e.notice
      }else if (currentRequirement>0 && currentRequirement < e.notice ){
        totalDropDown = currentRequirement
        afterTotal =   e.notice -currentRequirement
        newRow.commit_id = e.commit_id
        newRow.fund_id = e.fund_id
        newRow.invest_amount = totalDropDown
        newarr2.push(newRow)
        currentRequirement = 0
      } else{
        totalDropDown = 0
      }
      newRow.commit_id = e.commit_id
      newRow.fund_id = e.fund_id
      newRow.date = e.date
      newRow.fund = e.fund
      newRow.amount = toThousands(e.amount)
      newRow.notice = toThousands(e.notice)
      newRow.totalDropDown = toThousands(totalDropDown)
      newRow.afterTotal = toThousands(afterTotal)
      newarray.push(newRow)
    })
    setCalculateTable(newarray)
    setList(newarr2)
    // activate Button 
    setActive(false)

  }

  //  Submit call and fund investment
  const confirm = () =>{
    var investRequire = parseInt(callAmount)
    var formattedDate = new Date(date)
    var calledDate = formattedDate.getDate()+'/'+(formattedDate.getMonth()+1)+'/'+formattedDate.getFullYear()
    const data = {
      investName,
      investRequire,
      calledDate
    } 
    var url = "http://127.0.0.1:8000/calls/"
    // Create new call
    axios.post(url, data).then((res)=>{
      fundInvestList.forEach(e=>{
        // Then create each fund investment
        var commit_id = e.commit_id
        var fund_id = e.fund_id
        var  investAmount =e.invest_amount
        var call_id = callId + 1
        var req = {
          call_id,
          commit_id,
          fund_id,
          investAmount
        }
        var url = "http://127.0.0.1:8000/invests/"
        axios.post(url, req).then((res)=>{
          console.log(res.data)
          window.location.reload()
        }).catch(err=>{
          console.log(err)
        })
      })
    }).catch(err=>{
      console.log(err)
    })
  }

  useEffect (()=>{
    var url = "http://127.0.0.1:8000/calculate/"
      axios.get(url).then((res)=>{
        console.log(res.data)
        setTemporttable(res.data)
      }).catch((err)=>{
         console.log(err)
      })
  },[props.temporttable])

  return (
    <Container>
      <Form>
        <Form.Group controlId="formDate">
          <Form.Label>Date</Form.Label>
          <Form.Control type="date" onChange={e=>setDate(e.target.value)}/>
        </Form.Group>
        <Form.Group controlId="formRules">
          <Form.Label>Rules</Form.Label>
          <Form.Control as="select">
            <option>First in First Out (FIFO)</option>
            <option>Last-In First-Out (LIFO)</option>
          </Form.Control>
        </Form.Group>
        <Form.Group controlId="formInvestName">
          <Form.Label>Investment Name</Form.Label>
          <Form.Control type="text" placeholder="Please enter the investment name" onChange={e=>setInvestName(e.target.value)} />
        </Form.Group>
        <Form.Group controlId="formInvestAmount">
          <Form.Label>Capital Required for Investment</Form.Label>
          <Form.Control type="text" placeholder="Please enter the investment requirement" onChange={e=>setRequirement(e.target.value)} />
        </Form.Group>
        <Button variant="primary" type="button" onClick={count}>
          Calculate
        </Button>
      </Form>
      <Table className="mt-3">
        <thead>
          <tr>
            <th>commit_id</th>
            <th>fund_id</th>
            <th>date</th>
            <th>fund</th>
            <th>committed_amount</th>
            <th>Before Drawdown Notice</th>
            <th>Total Drawdown Notice</th>
            <th>After Drawdown Notice</th>
          </tr>
        </thead>
        <tbody>
          {calculateTable.map(e=>
          <tr>
            <th>{e.commit_id}</th>
            <th>{e.fund_id}</th>
            <th>{e.date}</th>
            <th>{e.fund}</th>
            <th>{e.amount}</th>
            <th>{e.notice!==0 ? e.notice:'-'}</th>
            <th>{e.totalDropDown!==0 ? e.totalDropDown:'-'}</th>
            <th>{e.afterTotal!==0 ? e.afterTotal:'-'}</th>
          </tr>
          )}
        </tbody>
      </Table>
      <Button type="submit" disabled={btnActive} onClick={confirm}>Confirm</Button>
    </Container>
   );
}

export default Callform