import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

import axios from 'axios';

const styles = theme => ({
    root: {
        width: '75%',
        marginTop: theme.spacing.unit * 3,
        overflowX: 'auto',
    },
    table: {
        minWidth: 700,
    },
});

class SimpleTable extends React.Component{

    state={
        data:[]
    };

    componentDidMount() {
        axios.get('http://127.0.0.1:8000/api')
            .then(res => {
                this.setState({data: res.data});
            })

    }


    render() {
    return (
        <Paper className={this.props.classes.root}>
            <Table className={this.props.classes.table}>
                <TableHead>
                    <TableRow>
                        <TableCell>id</TableCell>
                        <TableCell>Booked by</TableCell>
                        <TableCell align="right">Doctor Name</TableCell>
                        <TableCell align="right">Length of Visit</TableCell>
                        <TableCell align="right">Room</TableCell>
                        <TableCell align="right">Time</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {this.state.data.map(row => (
                        <TableRow key={row.id}>
                            <TableCell component="th" scope="row">
                                {row.id}
                            </TableCell>
                            <TableCell align="left">{row.booked_by}</TableCell>
                            <TableCell align="right">{row.doctor}</TableCell>
                            <TableCell align="right">{row.length}</TableCell>
                            <TableCell align="right">{row.room}</TableCell>
                            <TableCell align="right">{row.time}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </Paper>
    );
}


}

SimpleTable.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SimpleTable);
