import React from 'react';
import {Image,  Badge, Nav, Tab, Row} from 'react-bootstrap';
import logo from './logo.png'
import FundSummary from './FundSummary'
import {Callform} from '../NewCall'

const Dashboard = (props) =>{
   return (
      <Tab.Container defaultActiveKey="dashboard">
         <Nav variant="tabs" defaultActiveKey="dashboard">
            <Nav.Item className='mr-auto '><Image src={logo}></Image></Nav.Item>
            <Nav.Item className='mr-auto mt-4'>
               <Badge variant="primary ">
                  <h5 className="text-center">Capital Call</h5>
               </Badge>
            </Nav.Item>
            <Nav.Item className="mt-4"> 
               <Nav.Link  eventKey="dashboard">
                  <h5>Dashboard</h5>
               </Nav.Link>
            </Nav.Item>
            <Nav.Item className="mt-4">
               <Nav.Link eventKey="newcall">
                  <h5>New Call</h5>
               </Nav.Link>
            </Nav.Item>
         </Nav>
         <Tab.Content> 
            <Tab.Pane eventKey="dashboard">
               <FundSummary/>
            </Tab.Pane> 
         </Tab.Content>
         <Tab.Content > 
            <Tab.Pane eventKey="newcall">
               <Row className="p-5">
                  <Callform props={props}/>
               </Row>
            </Tab.Pane> 
         </Tab.Content>
      </Tab.Container>
   );
}

export default Dashboard