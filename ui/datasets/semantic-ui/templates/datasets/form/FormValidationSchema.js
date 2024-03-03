import * as Yup from "yup";

export const FormValidationSchema = Yup.object().shape({
  id: Yup.string().required(),
  // TODO: implement any yup form validations here
  // https://github.com/jquense/yup
});
