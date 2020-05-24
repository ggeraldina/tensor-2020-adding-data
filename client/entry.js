const add_booking = {
    "phone_number": "88005353535",
    "password_to_cancel": "password",
    "event": "000000000000000000000001",
    "tickets": [
        {"id": "000000000000000000000001"},
        {"id": "000000000000000000000002"},
        {"id": "000000000000000000000003"},
        {"id": "000000000000000000000004"}
    ]
};

const cancel_booking = {
  "id": "000000000000000000000007",
  "phone_number": "88005353535",
  "password_to_cancel": "password"
};


class Description extends React.Component {
  render() {
    return (
      <div>
      <section className="section">
        <div className="container">
          <h1 className="title is-1 has-text-centered">API tensor-2020</h1>

          <div className="tile is-ancestor">
            <div className="tile is-vertical is-parent">
              <div className="tile is-child box">              
                <h3 className="title has-text-centered">Получить список мероприятий</h3>
                <p className="has-text-centered">
                  <b>GET</b> /api/v1/get_events_list?offset=0&limit=1
                </p>
              </div>
              <div className="tile is-child box">
                <h3 className="title has-text-centered">Получить мероприятие</h3>
                <p className="has-text-centered">
                  <b>GET</b> /api/v1/get_event?id=000000000000000000000001
                </p>
              </div>
              <div className="tile is-child box">
                  <h3 className="title has-text-centered">Получить список броней</h3>
                  <p className="has-text-centered">
                    <b>GET</b> /api/v1/get_bookings_list?phone_number=88005353535
                  </p>
              </div>              
            </div>

            <div className="tile is-parent">
              <div className="tile is-child box">
                <h3 className="title has-text-centered">Забронировать</h3>
                <p className="has-text-centered"><b>POST</b> /api/v1/add_booking</p>
                <pre>json = {JSON.stringify(add_booking, undefined, 2)}</pre>  
              </div>
            </div>
            <div className="tile is-vertical is-parent">
              <div className="tile is-child box">
                <h3 className="title has-text-centered">Отменить бронь</h3>
                <p className="has-text-centered"><b>POST</b> /api/v1/canсel_booking</p>
                <pre>json = {JSON.stringify(cancel_booking, undefined, 2)}</pre>
              </div>
              <div className="tile is-child box">
                <h3 className="title has-text-centered">^.^</h3>
                <div className="image">
                  <img src="https://dagjournal.ru/uploads/posts/2019-10/1571731044_kotiki2-edit.jpeg"/>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <footer className="footer">
      <div className="content has-text-centered">
          <p>
              Для проекта tensor-2020         
          </p>
      </div>
      </footer>
      </div>
    );
  }
}


ReactDOM.render(
  <Description />,
  document.getElementById('root')
);
