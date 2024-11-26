// import React from 'react';
// import { Modal, Form, Input, Button } from 'antd';
// import axios from 'axios';
//
// // eslint-disable-next-line react/prop-types
// const RegisterModal = ({ visible, onClose }) => {
//     const handleRegister = async (values) => {
//         try {
//             const response = await axios.post('http://127.0.0.1/auth/register', {
//                 username: values.username,
//                 password: values.password,
//             });
//
//             if (response.status === 200) {
//                 alert('Регистрация прошла успешно!');
//                 onClose();
//             } else {
//                 alert(response.data.message);
//             }
//         } catch (error) {
//             alert('Ошибка регистрации: ' + (error.response.data.detail || 'Пожалуйста, попробуйте позже.'));
//         }
//     };
//
//     return (
//         <Modal
//             title="Регистрация"
//             visible={visible}
//             onCancel={onClose}
//             footer={null}
//             destroyOnClose={true}
//         >
//             <Form
//                 name="register"
//                 onFinish={handleRegister}
//                 layout="vertical"
//             >
//                 <Form.Item
//                     label="Имя пользователя"
//                     name="username"
//                     rules={[{ required: true, message: 'Пожалуйста, введите имя пользователя!' }]}
//                 >
//                     <Input />
//                 </Form.Item>
//                 <Form.Item
//                     label="Пароль"
//                     name="password"
//                     rules={[{ required: true, message: 'Пожалуйста, введите пароль!' }]}
//                 >
//                     <Input.Password />
//                 </Form.Item>
//                 <Form.Item>
//                     <Button type="primary" htmlType="submit">Зарегистрироваться</Button>
//                 </Form.Item>
//             </Form>
//         </Modal>
//     );
// };
//
// export default RegisterModal;
