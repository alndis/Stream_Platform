import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { Modal, Form, Input, Button } from 'antd';
import axios from 'axios';

function StreamModal({ stream, isVisible, onClose, onStreamUpdated, onStreamDeleted }) {
    const [form] = Form.useForm();
    const API_URL = "http://176.123.167.118:8000";
    const [isEditing, setIsEditing] = useState(false);

    const getVideoLink = (link) => {
        // Ваша функция получения ссылки на видео
        if (link == null || !link.startsWith("http")) return "https://rutube.ru/play/embed/f13ca0f6acdc7556c692c7a4d8f2a384";

        // Проверка на YouTube
        if (link.includes("youtube.com/watch?v=")) {
            const videoId = new URL(link).searchParams.get("v");
            return `https://www.youtube.com/embed/${videoId}`;
        } else if (link.includes("rutube.ru/video/")) {
            const videoId = link.split("/video/")[1].split("/")[0];
            return `https://rutube.ru/play/embed/${videoId}`;
        }
        return link;
    };

    const videoLink = getVideoLink(stream.link);

    // Обработчик редактирования стрима
    const handleEditStream = async () => {
        try {
            const token = localStorage.getItem('token');
            const values = form.getFieldsValue();
            console.log(stream.id, values);
            const updatedValues = {
                stream_id: stream.id,
                ...values // добавляем остальные поля из values
            };
            console.log(updatedValues);
            const response = await axios.put(`${API_URL}/api/streams/${stream.id}`, updatedValues, {
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.data.ok) {
                onStreamUpdated(); // Вызов функции обновления стримов
                setIsEditing(false);
                form.resetFields();
            }
        } catch (error) {
            console.error("Ошибка редактирования стрима:", error.response.data);
            alert('Ошибка редактирования стрима: '+ (error.response.data.detail || 'Пожалуйста, попробуйте позже.'));
        }
    };

    async function handleDeleteStream() {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                throw new Error("Токен не найден. Пожалуйста, войдите в систему.");
            }

            await axios.delete(`${API_URL}/api/streams/${stream.id}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            console.log("Стрим успешно удален");
            onStreamDeleted(); // Вызов функции для обновления списка стримов после удаления
        } catch (error) {
            alert("Ошибка удаления стрима: "+ (error.response.data.detail || 'Пожалуйста, попробуйте позже.'));
            console.error("Ошибка удаления стрима:", error.response ? error.response.data : error.message);
        }
    }



    return (
        <Modal
            visible={isVisible}
            onCancel={onClose}
            footer={null}
            width={800}
        >
            <iframe
                width="100%"
                height="400px"
                src={videoLink}
                title={stream.name || "Название стрима"}
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
            ></iframe>
            <div style={{ marginTop: '20px' }}>
                <h3>{stream.name || "Название стрима"}</h3>
                <p>{stream.description || "описание стрима"}</p>
                <Button onClick={() => setIsEditing(true)}>Редактировать</Button>
                <Button danger onClick={handleDeleteStream}>Удалить</Button>
            </div>

            {isEditing && (
                <Form form={form} initialValues={stream} style={{ marginTop: '20px' }}>
                    <Form.Item name="name" label="Название" rules={[{ required: true, message: 'Введите название стрима!' }]}>
                        <Input />
                    </Form.Item>
                    <Form.Item name="description" label="Описание" rules={[{ required: true, message: 'Введите описание стрима!' }]}>
                        <Input.TextArea />
                    </Form.Item>
                    <Form.Item name="preview" label="Ссылка на превью">
                        <Input />
                    </Form.Item>
                    <Form.Item name="link" label="Ссылка на видео">
                        <Input />
                    </Form.Item>
                    <Button type="primary" onClick={handleEditStream}>Сохранить изменения</Button>
                    <Button onClick={() => setIsEditing(false)}>Отмена</Button>
                </Form>
            )}
        </Modal>
    );
}

StreamModal.propTypes = {
    stream: PropTypes.shape({
        id: PropTypes.number.isRequired,
        name: PropTypes.string,
        description: PropTypes.string,
        preview: PropTypes.string,
        link: PropTypes.string,
    }).isRequired,
    isVisible: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    onStreamUpdated: PropTypes.func.isRequired,
    onStreamDeleted: PropTypes.func.isRequired,
};

export default StreamModal;
