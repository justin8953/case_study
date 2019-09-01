import React from 'react';
import {Image, Button, Container}from 'react-bootstrap';
import logo from './logo.png'

const Home = (props) =>{
   return (
      <div>
         <Image src={logo}/>
         <Container className="text-center ">
               <Button variant = "primary" size='lg' href="/dashboard">
                  <h1>Capital Call</h1>
               </Button>
         </Container>   
      </div>
   );
}

export default Home