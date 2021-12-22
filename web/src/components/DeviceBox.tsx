import {useState} from 'react'
import React from 'react'
import ReactDOM from 'react-dom'
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import DevicesManagement from './DevicesManagement'
import {RiSettings2Line} from "react-icons/ri"
import {Link} from 'react-router-dom'
import {toast} from "react-toastify";

interface DeviceBoxInterface {
  key: number;
  img: Element[];
  name: string;
  ipAddress: string;
  groupId: number;
  type: string;
  id: number;
  toggle: boolean;
  displayDevice: JSON,
}

class DeviceBox extends React.Component<DeviceBoxInterface, {}> {

  getCurrentState = () => {
    fetch(`/api/devices/${this.props.id}/status`, {
      method: "GET",
      headers: {
        'Content-type': 'application/json; charset=UTF-8'
      },
    })
      .then((response) => response.json())
      .then((json) => {
        this.setState({toggle: json.toggle});
      });
  }

  state: DeviceBoxInterface = {
    key: 0,
    img: [],
    name: "",
    ipAddress: "",
    groupId: 0,
    type: "",
    id: 0,
    toggle: false,
    displayDevice: JSON,
  }

  componentDidMount() {
    this.getCurrentState();
  }

  handleOnOff = () => {
    const newToggle = !this.state.toggle

    fetch(`/api/devices/${this.props.id}/${newToggle}`, {
      method: "PUT",
      headers: {
        'Content-type': 'application/json; charset=UTF-8'
      },
    })
      .then((response) => response.json())
      .then((json) => {

        fetch(`/api/devices/${this.props.id}/status`, {
          method: "GET",
          headers: {
            'Content-type': 'application/json; charset=UTF-8'
          },
        })
          .then((response) => response.json())
          .then((json) => {
            if (json.toggle != newToggle) {
              toast.error(`L'état de l'appareil n'a pas pu être changé`);
            }
            this.setState({toggle: json.toggle})
          });
      });
  }

  render() {
    return (
      <Col xxl={2} xl={4} lg={5} md={6} sm={7} xs={8}>
        <Card
          text='white'
          className="m-2"
        >
          <Card.Body>
            <Row>
              <Col>
                <Link to={"/Details/" + this.props.id} style={{textDecoration: 'none'}}>
                  <Card.Title>{this.props.img}{this.props.name}</Card.Title>
                  <Card.Text class="cardType">
                    {this.props.ipAddress}
                  </Card.Text>
                </Link>
              </Col>
              <Col>
                <Button
                  class="cardType"
                  variant={this.state.toggle ? "success" : "danger"}
                  onClick={this.handleOnOff}>{this.state.toggle ? "ON" : "OFF"}</Button>
              </Col>
            </Row>
          </Card.Body>
          <Card.Footer className="text-center">
            <DevicesManagement name={this.props.name} ipAddress={this.props.ipAddress} id={this.props.id}
                               groupId={this.props.groupId} type={this.props.type}
                               displayDevice={this.props.displayDevice} buttonFeature={<RiSettings2Line/>}
                               fetchMethod={"PUT"}/>
          </Card.Footer>
        </Card>
      </Col>
    );
  };
};

export default DeviceBox;