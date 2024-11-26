// import React from 'react';
// import { Modal, Form, Input, Button } from 'antd';
//
// // eslint-disable-next-line react/prop-types
// const LoginModal = ({ visible, onCancel, onFinish }) => {
//     return (
//         <Modal
//             title="Авторизация"
//             open={visible}
//             onCancel={onCancel}
//             footer={null}
//             destroyOnClose={true}
//         >
//             <Form
//                 name="login"
//                 onFinish={onFinish}
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
//                     <Button type="primary" htmlType="submit">
//                         Войти
//                     </Button>
//                 </Form.Item>
//             </Form>
//         </Modal>
//     );
// };
//
// export default LoginModal;
