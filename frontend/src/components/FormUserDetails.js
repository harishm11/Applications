import React, { Component } from 'react';
import AppBar from '@material-ui/core/AppBar';
import { ThemeProvider as MuiThemeProvider } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
// import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker';  

export class FormUserDetails extends Component {
  continue = e => {
    e.preventDefault();
    this.props.nextStep();
  };

  render() {
    const { values, handleChange } = this.props;
    return (
      <MuiThemeProvider>
          <AppBar
          fullWidth>
          Personal Details
          </AppBar>
            <TextField
              placeholder="Enter Your First Name"
              label="First Name"
              onChange={handleChange('firstName')}
              defaultValue={values.firstName}
              margin="normal"
              fullWidth
            />
            <br />
            <TextField
              placeholder="Enter Your Last Name"
              label="Last Name"
              onChange={handleChange('lastName')}
              defaultValue={values.lastName}
              margin="normal"
              fullWidth
            />
            <br />
            {/* <DesktopDatePicker
                label="Birth Date"
                inputFormat="MM/dd/yyyy"
                onChange={handleChange('birthDate')}
                defaultValue={values.birthDate}
                margin="normal"
                fullWidth
            /> */}
            <br />
            <Button
              color="primary"
              variant="contained"
              onClick={this.continue}
            >Continue</Button>
      </MuiThemeProvider>
    );
  }
}

export default FormUserDetails;
