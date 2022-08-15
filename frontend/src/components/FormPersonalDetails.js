import React, { Component } from 'react';
import AppBar from '@material-ui/core/AppBar';
import { ThemeProvider as MuiThemeProvider } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import Radio from '@mui/material/Radio';
import FormControlLabel from '@mui/material/FormControlLabel';

export class FormPersonalDetails extends Component {
  continue = e => {
    e.preventDefault();
    this.props.nextStep();
  };

  back = e => {
    e.preventDefault();
    this.props.prevStep();
  };

  render() {
    const { values, handleChange } = this.props;
    return (
      <MuiThemeProvider>
          <AppBar
          fullWidth>
            Marital Status
          </AppBar>
            <FormControl>
                <FormLabel>What's your Marital Status</FormLabel>
                <RadioGroup
                onChange={handleChange('maritalStatus')}
                defaultValue={values.maritalStatus}
                margin="normal"
                fullWidth
                >
                  <FormControlLabel value="Single" control={<Radio />} label="Single" />
                  <FormControlLabel value="Married" control={<Radio />} label="Married" />
                  <FormControlLabel value="Separated/Widowed" control={<Radio />} label="Separated/Widowed" />
                  
                </RadioGroup>
            </FormControl>
            <br />
            <Button
              color="white"
              variant="contained"
              onClick={this.back}
            >Back</Button>
            <Button
              color="primary"
              variant="contained"
              onClick={this.continue}
            >Continue</Button>
      </MuiThemeProvider>
    );
  }
}

export default FormPersonalDetails;
