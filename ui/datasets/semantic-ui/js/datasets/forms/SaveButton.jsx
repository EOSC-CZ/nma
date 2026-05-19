import { SaveButtonComponent } from "@js/oarepo_ui/forms/components/SaveButton/SaveButton";
import { save } from "./actions";
import { connect } from "react-redux";

const mapDispatchToProps = (dispatch) => ({
  saveAction: (values, params) => dispatch(save(values, params)),
});

const mapStateToProps = (state) => ({
  actionState: state.deposit.actionState,
});

export const SaveButton = connect(
  mapStateToProps,
  mapDispatchToProps
)(SaveButtonComponent);

export default SaveButton;
